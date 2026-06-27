#!/usr/bin/env python3
"""Generate Draw.io XML for activity connections from YAML input."""

from __future__ import annotations
from typing import Any

DRAWIO_XML_TEMPLATE_PHASE = '''
               <mxCell id="re-hWYANieQfaZoZakJm-{ref}" value="&lt;div style=&quot;line-height: 100%;&quot;&gt;&lt;font&gt;&lt;b&gt;{name}&lt;/b&gt;&lt;/font&gt;&lt;/div&gt;" style="html=1;whiteSpace=wrap;fillColor=#E6E6E6;container=1;rounded=1;absoluteArcSize=1;arcSize=24;fontSize=24;spacing=0;strokeColor=#666666;strokeOpacity=100;fillOpacity=100;strokeWidth=1.2;labelPosition=center;verticalLabelPosition=middle;align=center;verticalAlign=top;spacingTop=8;" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="{x}" y="100" width="{width}" height="{height}" as="geometry"/>
                </mxCell>
'''

def get_phases(data: dict[str, Any]) -> list[dict[str, str]]:
    """Return a list of phases from the YAML data.

    Each phase is normalized to a mapping with a `Name` key. If no `Phases`
    key is present an empty list is returned.
    """
    phases = data.get('Phases')
    if phases is None:
        return []
    if not isinstance(phases, list):
        raise ValueError('Phases must be a list')

    result: list[dict[str, str]] = []
    for index, item in enumerate(phases):
        if isinstance(item, dict):
            normalized = {key.lower(): value for key, value in item.items()}
            if 'name' not in normalized:
                raise ValueError('Each Phases item must be a string or mapping with a Name key')
            name = str(normalized['name'])
            width = str(normalized.get('width', 0))
        elif isinstance(item, str):
            name = item
            width = '0'
        else:
            raise ValueError('Each Phases item must be a string or mapping with a Name key')

        result.append({'Name': name, 'Width': width})
    return result

def add_phases_layer(metainformation: list[dict[str, str]], phases: list[dict[str, str]], START_X: int, START_Y: int, CELL_X: int, CELL_Y: int) -> str:
    """Return a Draw.io XML fragment for the given phases box."""
    result: list[str] = []
    xpos: int = 315
    width: int = 0
    ref: int = 3

    height = max((int)(metainformation[0]['Height']),(int)(metainformation[0]['MaxActivityRow']))

    height1 = height*CELL_Y+0.5*CELL_Y+START_Y
    height2=  (int)(metainformation[0]['NumberOfProcessGroups'])*40+START_Y

    for phase in phases:
        width = int(phase['Width'])*CELL_X-10
        result.append(
            DRAWIO_XML_TEMPLATE_PHASE.format(
                ref=ref,
                name=phase['Name'],
                width=width,
                height=max(height1,height2),
                x=xpos
            )
        )
        xpos += width+10
        ref += 1
    return ''.join(result)
