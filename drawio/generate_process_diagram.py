#!/usr/bin/env python3
"""Generate a Draw.io XML file matching SDLC Process Core.drawio."""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from unittest import result

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        'PyYAML is required to load the input YAML file. Install it with: pip install pyyaml'
    ) from exc

DRAWIO_XML_TEMPLATE_HEADER = '''<mxfile host="65bd71144e">
    <diagram name="SDLC Process" id="re-hWYANieQfaZoZakJm">
        <mxGraphModel dx="1882" dy="1139" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
            <root>
                 <mxCell id="0"/>
                <mxCell id="1" value="Main" style="locked=1;" parent="0"/>

                <mxCell id="re-hWYANieQfaZoZakJm-001" parent="1" style="html=1;whiteSpace=wrap;fillColor=none;container=1;rounded=1;absoluteArcSize=1;arcSize=24;fontSize=11;spacing=0;strokeOpacity=100;fillOpacity=0;strokeWidth=1.2;verticalAlign=top;" value="&lt;span style=&quot;font-size: 72px; font-weight: 700; text-align: left;&quot;&gt;Enterprise Application Development Lifecycle Reference Process&lt;/span&gt;" vertex="1">
                    <mxGeometry x="0" y="0" width="{width}" height="1150" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-002" value="&lt;span style=&quot;font-size: 24px; font-weight: 700;&quot;&gt;Legend&lt;/span&gt;" style="html=1;whiteSpace=wrap;;fontSize=11;spacing=0;strokeColor=#666666;strokeOpacity=100;fillOpacity=100;rounded=1;absoluteArcSize=1;arcSize=12;shadow=1;fillColor=#ffffff;strokeWidth=1.2;labelPosition=center;verticalLabelPosition=middle;align=left;verticalAlign=top;spacingTop=8;spacingLeft=15;" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="40" y="100" width="255" height="1000" as="geometry"/>
                </mxCell>

'''
DRAWIO_XML_TEMPLATE_PHASE = '''
               <mxCell id="re-hWYANieQfaZoZakJm-{ref}" value="&lt;div style=&quot;line-height: 100%;&quot;&gt;&lt;font&gt;&lt;b&gt;{name}&lt;/b&gt;&lt;/font&gt;&lt;/div&gt;" style="html=1;whiteSpace=wrap;fillColor=#E6E6E6;container=1;rounded=1;absoluteArcSize=1;arcSize=24;fontSize=24;spacing=0;strokeColor=#666666;strokeOpacity=100;fillOpacity=100;strokeWidth=1.2;labelPosition=center;verticalLabelPosition=middle;align=center;verticalAlign=top;spacingTop=8;" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="{x}" y="100" width="{width}" height="1000" as="geometry"/>
                </mxCell>
'''

DRAWIO_XML_TEMPLATE_ACTIVITIES_LAYER = '''
                <mxCell id="re-hWYANieQfaZoZakJm-100" value="Activities" style="locked=1;" parent="0"/>
'''

DRAWIO_XML_TEMPLATE_FOOTER = '''
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
'''

DEFAULT_PROCESS_GROUPS = [
    {'Name': 'Application Development Core Process', 'Color': '#19967D'},
 ]

DEFAULT_ACTIVITIES = [
    {'Name': 'Activity', 'ProcessGroup': 'Application Development Core Process', 'ID': 'activity', 'PHASE': 'Plan', 'X': '1', 'Y': '1'},
 ]

DRAWIO_XML_TEMPLATE_PROCESSGROUPS = '''
                <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" value="{group}" style="html=1;whiteSpace=wrap;fontSize=11;fontColor=#000000;align=left;spacing=0;verticalAlign=middle;strokeOpacity=100;fillOpacity=100;fillColor=none;strokeWidth=3.5999999999999996;strokeColor=none;" vertex="1" parent="re-hWYANieQfaZoZakJm-001">
                    <mxGeometry x="113.43588925629517" y="{ypos1}" width="150" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" value="" style="html=1;whiteSpace=wrap;;fontSize=11;align=center;spacingTop=9;spacing=5;verticalAlign=bottom;strokeOpacity=0;fillOpacity=100;rounded=1;absoluteArcSize=1;arcSize=109.2;fillColor={color};strokeWidth=0.6;strokeColor={color};" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="55.73952657838265" y="{ypos2}" width="25" height="25" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-{ref3}" value="" style="html=1;whiteSpace=wrap;;fontSize=11;align=center;spacingTop=9;spacing=5;verticalAlign=bottom;strokeOpacity=0;fillOpacity=100;rounded=1;absoluteArcSize=1;arcSize=109.2;fillColor=#ffffff;strokeWidth=0.6;strokeColor={color};" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="62.03367523415494" y="{ypos3}" width="12.5" height="12.5" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-{ref4}" value="" style="html=1;jettySize=18;fontSize=11;strokeColor={color};strokeOpacity=100;strokeWidth=6;rounded=1;arcSize=0;startArrow=none;endArrow=none;" parent="re-hWYANieQfaZoZakJm-001" edge="1">
                    <mxGeometry width="100" height="100" relative="1" as="geometry">
                        <mxPoint x="77.76904687358562" y="{ypos4}" as="sourcePoint"/>
                        <mxPoint x="96.65149284090243" y="{ypos4}" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
'''

DRAWIO_XML_TEMPLATE_ACTIVITY = '''
                <!-- Grouping element-->
                <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" connectable="0" parent="re-hWYANieQfaZoZakJm-100" style="group;strokeColor=none;strokeWidth=1;fontSize=12;" value="" vertex="1">
                <mxGeometry height="80" width="80" x="{xpos}" y="{ypos}" as="geometry" />
                </mxCell>
                <!-- Text element -->
                <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" parent="re-hWYANieQfaZoZakJm-{ref1}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeColor={color};strokeWidth=10;fillColor=#ffffff;gradientColor=none;align=center;verticalAlign=top;fontSize=12;spacingTop=12;" value="&lt;h5 style=&quot;font-size: 12px;&quot;&gt;{name}&lt;/h5&gt;" vertex="1">
                <mxGeometry height="30" width="30" x="0" y="25" as="geometry" />
                </mxCell>
'''

DRAWIO_XML_TEMPLATE_CONNECTION_CURVED_DOWN = '''
                <!-- Connection element-->
                <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" edge="1" parent="re-hWYANieQfaZoZakJm-100" source="re-hWYANieQfaZoZakJm-{ref2}" style="html=1;jettySize=18;fontSize=11;strokeColor={color};strokeOpacity=100;strokeWidth=10;arcSize=0;startArrow=none;endArrow=none;curved=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" target="re-hWYANieQfaZoZakJm-{ref3}" value="">
                    <mxGeometry width="100" height="100" relative="1" as="geometry">
                        <Array as="points">
                            <mxPoint x="{x3}" y="{y1}"/>
                            <mxPoint x="{x3}" y="{y2}"/>
                        </Array>
                        <mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>
                        <mxPoint x="{x2}" y="{y2}" as="targetPoint"/>
                    </mxGeometry>

                    <mxGeometry height="50" relative="1" width="50" as="geometry">
                        <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
                        <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
                    </mxGeometry>
                </mxCell>
'''

DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT = '''
        <!-- Connection element-->
        <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" edge="1" parent="re-hWYANieQfaZoZakJm-100" source="re-hWYANieQfaZoZakJm-{ref2}" style="endArrow=none;html=1;exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;strokeWidth=10;fillColor=#e3c800;strokeColor={color};rounded=0;" target="re-hWYANieQfaZoZakJm-{ref3}" value="">
            <mxGeometry height="50" relative="1" width="50" as="geometry">
                <mxPoint x="{x1}" y="{y1}" as="sourcePoint" />
                <mxPoint x="{x2}" y="{y2}" as="targetPoint" />
            </mxGeometry>
        </mxCell>
'''

DRAWIO_XML_TEMPLATE_CONNECTION_LU = '''
        <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" connectable="0" parent="re-hWYANieQfaZoZakJm-100" style="group" value="" vertex="1">
          <mxGeometry height="80" width="80" x="{x1}" y="{y1}" as="geometry" />
        </mxCell>
        <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" edge="1" parent="re-hWYANieQfaZoZakJm-{ref1}" style="endArrow=none;html=1;exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;strokeWidth=10;fillColor=#e51400;strokeColor={color};curved=1;rounded=0;" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <Array as="points">
              <mxPoint x="40" y="40" />
            </Array>
            <mxPoint x="40" y="80" as="sourcePoint" />
            <mxPoint y="40" as="targetPoint" />
          </mxGeometry>
        </mxCell>
'''
DRAWIO_XML_TEMPLATE_CONNECTION_UR = '''
        <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" connectable="0" parent="re-hWYANieQfaZoZakJm-100" style="group" value="" vertex="1">
          <mxGeometry height="80" width="80" x="{x1}" y="{y1}" as="geometry" />
        </mxCell>
        <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" edge="1" parent="re-hWYANieQfaZoZakJm-{ref1}" style="endArrow=none;html=1;exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;strokeWidth=10;fillColor=#e51400;strokeColor={color};curved=1;rounded=0;" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <Array as="points">
              <mxPoint x="40" y="40" />
            </Array>
            <mxPoint x="80" y="40" as="sourcePoint" />
            <mxPoint x="40" as="targetPoint" />
          </mxGeometry>
        </mxCell>
'''

DRAWIO_XML_TEMPLATE_CONNECTION_LO = '''
        <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" connectable="0" parent="re-hWYANieQfaZoZakJm-100" style="group" value="" vertex="1">
          <mxGeometry height="80" width="80" x="{x1}" y="{y1}" as="geometry" />
        </mxCell>
        <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" edge="1" parent="re-hWYANieQfaZoZakJm-{ref1}" style="endArrow=none;html=1;exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;strokeWidth=10;fillColor=#e51400;strokeColor={color};curved=1;rounded=0;" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <Array as="points">
              <mxPoint x="40" y="40" />
            </Array>
            <mxPoint x="40" y="0" as="sourcePoint" />
            <mxPoint x="0" y="40" as="targetPoint" />
          </mxGeometry>
        </mxCell>
'''
DRAWIO_XML_TEMPLATE_CONNECTION_OR = '''
        <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" connectable="0" parent="re-hWYANieQfaZoZakJm-100" style="group" value="" vertex="1">
          <mxGeometry height="80" width="80" x="{x1}" y="{y1}" as="geometry" />
        </mxCell>
        <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" edge="1" parent="re-hWYANieQfaZoZakJm-{ref1}" style="endArrow=none;html=1;exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;strokeWidth=10;fillColor=#e51400;strokeColor={color};curved=1;rounded=0;" value="">
          <mxGeometry height="50" relative="1" width="50" as="geometry">
            <Array as="points">
              <mxPoint x="40" y="40" />
            </Array>
            <mxPoint x="40" y="80" as="sourcePoint" />
            <mxPoint x="80" y="40" as="targetPoint" />
          </mxGeometry>
        </mxCell>
'''
DRAWIO_XML_TEMPLATE_CONNECTION_COMMENT = '''
        <!-- Connection from {source_id} to {target_id} -->
'''

START_X = 240
START_Y = 70  
CELL_X = 110
CELL_Y = 90

def add_activityconnections2(activityconnections: list[dict[str, str]], activities: list[dict[str, str]], process_groups: list[dict[str, str]]) -> str:
    """Return a Draw.io XML fragment for the given activity connections."""
    result: list[str] = []
    ref: int = 401
    for connection in activityconnections:
        source_id = connection['Source']
        target_id = connection['Target']
        routing = int(connection['Routing'])
        source_activity = next((a for a in activities if a.get('ID') == source_id), None)
        target_activity = next((a for a in activities if a.get('ID') == target_id), None)
        processgroup = next((g for g in process_groups if g.get('Name') == connection.get('ProcessGroup')), None)

        source_x = int(source_activity.get('X', 1))
        source_y = int(source_activity.get('Y', 1))
        target_x = int(target_activity.get('X', 1))
        target_y = int(target_activity.get('Y', 1))
        routing = min(routing,target_x-source_x)

        result.append(
            DRAWIO_XML_TEMPLATE_CONNECTION_COMMENT.format(
                source_id=source_id,
                target_id=target_id
            )
        )

        if (source_x == target_x and source_y < target_y): # Vertical Line    
            x1 = START_X + source_x * CELL_X + 20
            y1 = START_Y + source_y * CELL_Y + 40
            x2 = START_X + target_x * CELL_X + 20
            y2 = START_Y + target_y * CELL_Y + 0
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref,
                    ref2=source_activity['ID'],
                    ref3=target_activity['ID'],
                    color= processgroup['Color'],
                    exit_x=0.5,
                    exit_y=1,
                    entry_x=0.5,
                    entry_y=0,
                    x1=x1,
                    x2=x2,
                    y1=y1,
                    y2=y2
                )
            )
        elif (source_y == target_y  and source_x < target_x): # Horizontal Line    
            x1 = START_X + source_x * CELL_X + 40
            y1 = START_Y + source_y * CELL_Y + 20
            x2 = START_X + target_x * CELL_X + 0
            y2 = START_Y + target_y * CELL_Y + 20
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref,
                    ref2=source_activity['ID'],
                    ref3=target_activity['ID'],
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0,
                    entry_y=0.5,
                    x1=x1,
                    x2=x2,
                    y1=y1,
                    y2=y2
                )
            )
        elif (source_x < target_x and source_y < target_y): # Line down and then right
            x1 = START_X + source_x * CELL_X + 30
            y1 = START_Y + source_y * CELL_Y + 0
            x2 = START_X + target_x * CELL_X + 0
            y2 = START_Y + target_y * CELL_Y + 0
            if (routing>1):
                # Horizontale Linie
                result.append(
                    DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                        ref1=ref+6,
                        ref2=source_activity['ID'],
                        ref3=ref,
                        color= processgroup['Color'],
                        exit_x=1,
                        exit_y=0.5,
                        entry_x=0,
                        entry_y=0.5,
                        x1=x1,
                        x2=x1+CELL_X*(routing-1),
                        y1=y1,
                        y2=y1
                    )
                )
                x1+=CELL_X*(routing-1)

            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_LU.format(
                    ref1=ref,
                    ref2=ref+1,
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0.5,
                    entry_y=0.5,
                    x1=x1,
                    y1=y1
                )
            )
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_UR.format(
                    ref1=ref+2,
                    ref2=ref+3,
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0.5,
                    entry_y=0.5,
                    x1=x1,
                    y1=y2
                )
            )
            # Senkrechte Linie
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref+4,
                    ref2=ref,
                    ref3=ref+2,
                    color= processgroup['Color'],
                    exit_x=0.5,
                    exit_y=1,
                    entry_x=0.5,
                    entry_y=0,
                    x1=x1+40,
                    x2=x1+40,
                    y1=y1+CELL_Y,
                    y2=y2-80
                )
            )
            # Horizontale Linie
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref+5,
                    ref2=ref+2,
                    ref3=target_activity['ID'],
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0,
                    entry_y=0.5,
                    x1=x1+CELL_X,
                    x2=x2,
                    y1=y2,
                    y2=y2
                )
            )
        elif (source_x < target_x and source_y > target_y): # Line up and then right
            x1 = START_X + source_x * CELL_X + 30
            y1 = START_Y + source_y * CELL_Y + 0
            x2 = START_X + target_x * CELL_X + 0
            y2 = START_Y + target_y * CELL_Y + 0
            if (routing>1):
                # Horizontale Linie
                result.append(
                    DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                        ref1=ref+6,
                        ref2=source_activity['ID'],
                        ref3=ref,
                        color= processgroup['Color'],
                        exit_x=1,
                        exit_y=0.5,
                        entry_x=0,
                        entry_y=0.5,
                        x1=x1,
                        x2=x1+CELL_X*(routing-1),
                        y1=y1,
                        y2=y1
                    )
                )
                x1+=CELL_X*(routing-1)
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_LO.format(
                    ref1=ref,
                    ref2=ref+1,
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0.5,
                    entry_y=0.5,
                    x1=x1,
                    y1=y1
                )
            )

            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_OR.format(
                    ref1=ref+2,
                    ref2=ref+3,
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0.5,
                    entry_y=0.5,
                    x1=x1,
                    y1=y2
                )
            )

            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref+4,
                    ref2=ref,
                    ref3=ref+2,
                    color= processgroup['Color'],
                    exit_x=0.5,
                    exit_y=0,
                    entry_x=0.5,
                    entry_y=1,
                    x1=x1+40,
                    x2=x1+40,
                    y1=y1-CELL_Y,
                    y2=y2+80
                )
            )
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref+5,
                    ref2=ref+2,
                    ref3=target_id,
                    color= processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0,
                    entry_y=0.5,
                    x1=x1+CELL_X,
                    x2=x2,
                    y1=y2,
                    y2=y2
                )
            )

        ref += 7

    return ''.join(result)

def add_activities(activities: list[dict[str, str]], process_groups: list[dict[str, str]]) -> str:
    """Return a Draw.io XML fragment for the given activities."""
    result: list[str] = []
    ref: int = 101
    for activity in activities:
        # Look up the process group by its Name (the YAML stores the group name)
        group_name = activity.get('ProcessGroup')
        process_group = None
        if isinstance(group_name, str):
            process_group = next((g for g in process_groups if g.get('Name') == group_name), None)
        # If not found, try interpreting the ProcessGroup as an index
        if process_group is None:
            try:
                idx = int(group_name) if group_name is not None else None
            except Exception:
                idx = None
            if idx is not None and 0 <= idx < len(process_groups):
                process_group = process_groups[idx]
        # Final fallback to first defined process group or default
        if process_group is None:
            process_group = process_groups[0] if process_groups else DEFAULT_PROCESS_GROUPS[0]

        xpos: int = START_X + int(activity.get('X', 1)) * CELL_X
        ypos: int = START_Y + int(activity.get('Y', 1)) * CELL_Y

        result.append(
            DRAWIO_XML_TEMPLATE_ACTIVITY.format(
                name=activity['Name'],
                color=process_group['Color'],
                xpos=xpos,
                ypos=ypos,
                ref1=ref+1,
                ref2=activity['ID']
            )
        )
        ypos += 40
        ref += 1
    return ''.join(result)

def add_process_groups(process_groups: list[dict[str, str]]) -> str:
    """Return a Draw.io XML fragment for the given process groups."""
    result: list[str] = []
    ypos: int = 150
    ref: int = 20
    for process_group in process_groups:
        result.append(
            DRAWIO_XML_TEMPLATE_PROCESSGROUPS.format(
                group=process_group['Name'],
                color=process_group['Color'],
                ypos1=ypos,
                ypos2=ypos+7.5,
                ypos3=ypos+13.75,
                ypos4=ypos+20,
                ref1=ref,
                ref2=ref+1,
                ref3=ref+2,
                ref4=ref+3
            )
        )
        ypos += 40
        ref += 4
    return ''.join(result)

def add_phases(phases: list[dict[str, str]]) -> str:
    """Return a Draw.io XML fragment for the given phases box."""
    result: list[str] = []
    xpos: int = 315
    width: int = 0
    ref: int = 3

    # Compute total width as the sum of all phase widths (in pixels)
    totalwidth = 0
    for phase in phases:
        phase_w = int(phase.get('Width', 1))
        totalwidth += phase_w

    totalwidth= xpos + totalwidth*CELL_X + 30

    result.append(
        DRAWIO_XML_TEMPLATE_HEADER.format(
            width=totalwidth
        )
    )

    for phase in phases:
        width = int(phase['Width'])*CELL_X-10
        result.append(
            DRAWIO_XML_TEMPLATE_PHASE.format(
                ref=ref,
                name=phase['Name'],
                width=width,
                x=xpos
            )
        )
        xpos += width+10
        ref += 1
    return ''.join(result)

def load_yaml(path: Path) -> dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f'Expected YAML mapping at top level in {path}')
    return data


def get_process_groups(data: dict[str, Any]) -> list[dict[str, str]]:
    groups = data.get('ProcessGroups')
    if groups is None:
        raise ValueError('YAML must contain a top-level ProcessGroups key')
    if not isinstance(groups, list):
        raise ValueError('ProcessGroups must be a list')

    process_groups: list[dict[str, str]] = []
    for index, item in enumerate(groups):
        if isinstance(item, dict):
            normalized = {key.lower(): value for key, value in item.items()}
            if 'name' not in normalized:
                raise ValueError('Each ProcessGroups item must be a string or mapping with a Name key')

            name = str(normalized['name'] or DEFAULT_PROCESS_GROUPS[index]['Name'])
            color = str(normalized.get('color') or DEFAULT_PROCESS_GROUPS[index]['Color'])
        elif isinstance(item, str):
            name = DEFAULT_PROCESS_GROUPS[index]['Name']
            color = DEFAULT_PROCESS_GROUPS[index]['Color']
        else:
            raise ValueError('Each ProcessGroups item must be a string or mapping with a Name key')

        process_groups.append({'Name': name, 'Color': color})
    return process_groups

def get_activities(data: dict[str, Any]) -> list[dict[str, str]]:
    activities = data.get('Activities')
    if activities is None:
        raise ValueError('YAML must contain a top-level Activities key')
    if not isinstance(activities, list):
        raise ValueError('Activities must be a list')
    
    result: list[dict[str, str]] = []
    for index,item in enumerate(activities):
        if isinstance(item, dict):
            normalized = {key.lower(): value for key, value in item.items()}
            if 'name' not in normalized:
                raise ValueError('Each Activity item must have a Name key')
            

            name = str(normalized['name'] or DEFAULT_ACTIVITIES[index]['Name'])
            processgroup = str(normalized.get('processgroup') or DEFAULT_ACTIVITIES[index]['ProcessGroup'])
            id = str(normalized.get('id') or DEFAULT_ACTIVITIES[index]['ID'])
            phase = str(normalized.get('phase') or DEFAULT_ACTIVITIES[index]['PHASE'])
            x = str(normalized.get('x') or DEFAULT_ACTIVITIES[index]['X'])
            y = str(normalized.get('y') or DEFAULT_ACTIVITIES[index]['Y'])
        elif isinstance(item, str):
            name = DEFAULT_ACTIVITIES[index]['Name']
            processgroup = DEFAULT_ACTIVITIES[index]['ProcessGroup']
            id = DEFAULT_ACTIVITIES[index]['ID']
            phase = DEFAULT_ACTIVITIES[index]['Phase']
            x = DEFAULT_ACTIVITIES[index]['X']
            y = DEFAULT_ACTIVITIES[index]['Y']
        else:
            raise ValueError('Each Activity item must be a mapping with a Name key')
    
        result.append({'Name': name, 'ProcessGroup': processgroup, 'ID': id, 'Phase': phase, 'X': x, 'Y': y})
    return result


def get_activityconnections(data: dict[str, Any]) -> list[dict[str, str]]:
    """Return a list of activity connection mappings from the YAML data.

    Each connection is normalized to a mapping with string keys: `ID`, `Source`,
    and `Target`. If no ActivityConnections key is present an empty list is
    returned.
    """
    connections = data.get('ActivityConnections')
    if connections is None:
        return []
    if not isinstance(connections, list):
        raise ValueError('ActivityConnections must be a list')

    result: list[dict[str, str]] = []
    for index, item in enumerate(connections):
        if isinstance(item, dict):
            normalized = {key.lower(): value for key, value in item.items()}
            if 'source' not in normalized or 'target' not in normalized:
                raise ValueError('Each ActivityConnections item must contain Source and Target keys')

            conn_id = str(normalized.get('id') or index + 1)
            source = str(normalized.get('source'))
            target = str(normalized.get('target'))
            routing_value = normalized.get('routing', 1)
            routing = str(routing_value if routing_value is not None else 1)
            processgroup = str(normalized.get('processgroup'))
        else:
            raise ValueError('Each ActivityConnections item must be a mapping with Source and Target')

        result.append({'ID': conn_id, 'Source': source, 'Target': target, 'ProcessGroup': processgroup, 'Routing': routing})
    return result


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
            width = str(normalized['width'])
        elif isinstance(item, str):
            name = item
        else:
            raise ValueError('Each Phases item must be a string or mapping with a Name key')

        result.append({'Name': name, 'Width': width})
    return result

def write_drawio(path: Path, xml: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write(xml)


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


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    yaml_data = load_yaml(input_path)
    phases = get_phases(yaml_data)
    process_groups = get_process_groups(yaml_data)
    activities = get_activities(yaml_data)
    activityconnections = get_activityconnections(yaml_data)
    output_path = Path(args.output)
    write_drawio(output_path, add_phases(phases)+
                              add_process_groups(process_groups) +
                              DRAWIO_XML_TEMPLATE_ACTIVITIES_LAYER +
                              add_activityconnections2(activityconnections, activities, process_groups) +
                              add_activities(activities, process_groups) +
                              DRAWIO_XML_TEMPLATE_FOOTER)
    print(f'Generated {output_path.resolve()} using {input_path}')

if __name__ == '__main__':
    main()
