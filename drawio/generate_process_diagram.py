# -i .\enterprise-application-delivery-lifecycle-process\sample\meta_model\sample_enterprise_application_delivery_lifecycle_process.yaml -o .\enterprise-application-delivery-lifecycle-process\sample\diagram\sample-enterprise-application-delivery-lifecycle-process.drawio
#!/usr/bin/env python3
"""Generate a Draw.io XML file matching SDLC Process Core.drawio."""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any

try:
    from . import phases as phases_module
    from . import activities as activities_module
    from . import process_groups as process_groups_module
except ImportError:
    import phases as phases_module
    import activities as activities_module
    import process_groups as process_groups_module

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        'PyYAML is required to load the input YAML file. Install it with: pip install pyyaml'
    ) from exc

START_X = 240
START_Y = 70  

DRAWIO_XML_TEMPLATE_HEADER = '''<mxfile host="65bd71144e">
    <diagram name="SDLC Process" id="re-hWYANieQfaZoZakJm">
        <mxGraphModel dx="1882" dy="1139" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
            <root>
                 <mxCell id="0"/>
                <mxCell id="1" value="Main" style="locked=1;" parent="0"/>

                <mxCell id="re-hWYANieQfaZoZakJm-001" parent="1" style="html=1;whiteSpace=wrap;fillColor=none;container=1;rounded=1;absoluteArcSize=1;arcSize=24;fontSize=11;spacing=0;strokeOpacity=100;fillOpacity=0;strokeWidth=1.2;verticalAlign=top;" value="&lt;span style=&quot;font-size: 72px; font-weight: 700; text-align: left;&quot;&gt;{name}&lt;/span&gt;" vertex="1">
                    <mxGeometry x="0" y="0" width="{width}" height="{height2}" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-002" value="&lt;span style=&quot;font-size: 24px; font-weight: 700;&quot;&gt;Legend&lt;/span&gt;" style="html=1;whiteSpace=wrap;;fontSize=11;spacing=0;strokeColor=#666666;strokeOpacity=100;fillOpacity=100;rounded=1;absoluteArcSize=1;arcSize=12;shadow=1;fillColor=#ffffff;strokeWidth=1.2;labelPosition=center;verticalLabelPosition=middle;align=left;verticalAlign=top;spacingTop=8;spacingLeft=15;" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="40" y="100" width="255" height="{height1}" as="geometry"/>
                </mxCell>
'''

DRAWIO_XML_TEMPLATE_FOOTER = '''
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
'''


def add_header(metainformation: list[dict[str, str]], phases: list[dict[str, str]], process_groups: list[dict[str, str]], activities: list[dict[str, str]]) -> str:
    """Return a Draw.io XML fragment for the given phases box."""
    result: list[str] = []
    xpos: int = 315

    # Compute total width as the sum of all phase widths (in pixels)
    totalwidth = 0
    for phase in phases:
        phase_w = int(phase.get('Width', 1))
        totalwidth += phase_w

    totalwidth= max(xpos + totalwidth*activities_module.CELL_X + 30, 1000)
    height = max((int)(metainformation[0]['Height']),(int)(metainformation[0]['MaxActivityRow']))


    height1 = height*activities_module.CELL_Y+0.5*activities_module.CELL_Y+START_Y
    height2=  (int)(metainformation[0]['NumberOfProcessGroups'])*40+START_Y

    name = metainformation[0]['Name'] if metainformation else 'Missing Name'
    result.append(
        DRAWIO_XML_TEMPLATE_HEADER.format(
            width=totalwidth,
            name=name,
            height1=max(height1, height2),
            height2=max(height1, height2)+150
        )
    )

    return ''.join(result)

def get_meta_information(data: dict[str, Any]) -> list[dict[str, str]]:
    """Return a list of normalized MetaInformation entries from the YAML data.

    If no MetaInformation key is present, an empty list is returned.
    MetaInformation may be a single mapping or a list of mappings.
    Each entry must contain a Name key and is normalized to string values.
    """
    result: list[dict[str, str]] = []

    meta_information = data.get('MetaInformation')
    if meta_information is None:
        result.append({'Name': 'Missing Name', 'Height': '0'})
        return result
    if isinstance(meta_information, dict):
        meta_information = [meta_information]
    elif not isinstance(meta_information, list):
        raise ValueError('MetaInformation must be a mapping or list')

    item = meta_information[0]
    if isinstance(item, dict):
            normalized = {key.lower(): value for key, value in item.items()}
            name = str(normalized['name'])
            height = str(normalized.get('height', 0))
    elif isinstance(item, str):
        name = 'Missing title'
        height = '0'
    else:
        raise ValueError('Each MetaInformation item must be a string or mapping')

    result.append({'Name': name, 'Height': height})

    return result

def calculate_width_for_phases(activities: list[dict[str, str]], phases: list[dict[str, str]]) -> dict[str, int]:
    """Return the maximum X position for every phase defined in phases."""
    result: dict[str, int] = {}
    width: int = 0

    for phase in phases:
        phase_name = str(phase.get('Name', '')).strip()
        if not phase_name:
            continue
        max_x = activities_module.get_max_activity_x_for_phase(activities, phase_name)
        result[phase_name] = max_x - width
        width = max_x

    return result


def enhance_meta_information(metainformation: list[dict[str, str]], process_groups: list[dict[str, str]], phases: list[dict[str, str]], activities: list[dict[str, str]]) -> list[dict[str, str]]:
    """Add additional meta-information derived from process groups and activities.
    
    Adds the process group count, maximum activity Y position, and maximum X
    for activities in the Continuous Exploration phase to the first
    metainformation entry.
    """
    if not metainformation:
        return metainformation
    
    process_group_count = process_groups_module.count_process_groups(process_groups)
    metainformation[0]['NumberOfProcessGroups'] = str(process_group_count)

    max_activity_row = activities_module.get_max_activity_row(activities)
    metainformation[0]['MaxActivityRow'] = str(max_activity_row)

    phase_widths = calculate_width_for_phases(activities, phases)
    
    i: int = 0
    for phase in phases:
        defined_phase_width = int(phase.get('Width', 0))
        calculated_phase_width = phase_widths[phase.get('Name')]
        max_phase_width = max(defined_phase_width, calculated_phase_width)
        if (defined_phase_width!=0 and defined_phase_width<calculated_phase_width): 
            print(f'Defined Width for {phase.get('Name')} changed from {defined_phase_width} to {calculated_phase_width}')

        phase['Width'] = max_phase_width

    return metainformation


def write_drawio(path: Path, xml: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write(xml)

def load_yaml(path: Path) -> dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f'Expected YAML mapping at top level in {path}')
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate SDLC Process Core.drawio XML file.')
    parser.add_argument(
        '--output', '-o',
        default='SDLC Process Core.generated.drawio',
        help='Output .drawio filename (default: SDLC Process Core.generated.drawio)'
    )
    parser.add_argument(
        '--input', '-i',
        default='SDLC Process.yaml',
        help='Input .yaml filename with process configuration (default: SDLC Process.yaml)'
    )
    return parser.parse_args()

def generate_drawio(input_path: Path, output_path: Path) -> None:
    yaml_data = load_yaml(input_path)
    metainformation = get_meta_information(yaml_data)
    phases = phases_module.get_phases(yaml_data)
    process_groups = process_groups_module.get_process_groups(yaml_data)
    activities = activities_module.get_activities(yaml_data)
    activityconnections = activities_module.get_activityconnections(yaml_data)

    enhance_meta_information(metainformation, process_groups, phases, activities)

    write_drawio(output_path, add_header(metainformation, phases, process_groups, activities)+
                              phases_module.add_phases_layer(metainformation, phases, START_X, START_Y, activities_module.CELL_X, activities_module.CELL_Y)+
                              process_groups_module.add_process_group_layer(process_groups) +
                              activities_module.add_activities_layer(activityconnections, activities, process_groups, START_X, START_Y) +
                              DRAWIO_XML_TEMPLATE_FOOTER)
    print(f'Generated {output_path.resolve()} using {input_path}')

def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    generate_drawio(input_path, output_path)

if __name__ == '__main__':
    main()
