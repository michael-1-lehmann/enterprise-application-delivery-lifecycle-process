#!/usr/bin/env python3
"""Generate Draw.io XML for activities and activity connections from YAML input."""

from __future__ import annotations
from typing import Any
from unittest import result

CELL_X = 110
CELL_Y = 90

DRAWIO_XML_TEMPLATE_ACTIVITIES_LAYER = '''
                <mxCell id="re-hWYANieQfaZoZakJm-100" value="Activities" style="locked=1;" parent="0"/>
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

DRAWIO_XML_TEMPLATE_CONNECTION_COMMENT = '''
        <!-- Connection from {source_id} to {target_id} -->
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
        else:
            raise ValueError('Each Activity item must be a mapping with a Name key')
    
        result.append({'Name': name, 'ProcessGroup': processgroup, 'ID': id, 'Phase': phase, 'X': x, 'Y': y})
    return result

def get_activityconnections(data: dict[str, Any]) -> list[dict[str, str]]:
    """Return a list of activity connection mappings from the YAML data."""
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


def add_activityconnections(activityconnections: list[dict[str, str]], activities: list[dict[str, str]], process_groups: list[dict[str, str]], START_X: int, START_Y: int) -> str:
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

        if source_activity is None or target_activity is None or processgroup is None:
            raise ValueError(f'Invalid activity connection: {connection}')

        source_x = int(source_activity.get('X', 1))
        source_y = int(source_activity.get('Y', 1))
        target_x = int(target_activity.get('X', 1))
        target_y = int(target_activity.get('Y', 1))
        routing = min(routing, target_x - source_x)

        result.append(
            DRAWIO_XML_TEMPLATE_CONNECTION_COMMENT.format(
                source_id=source_id,
                target_id=target_id
            )
        )

        if source_x == target_x and source_y < target_y:
            x1 = START_X + source_x * CELL_X + 20
            y1 = START_Y + source_y * CELL_Y + 40
            x2 = START_X + target_x * CELL_X + 20
            y2 = START_Y + target_y * CELL_Y + 0
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref,
                    ref2=source_activity['ID'],
                    ref3=target_activity['ID'],
                    color=processgroup['Color'],
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
        elif source_y == target_y and source_x < target_x:
            x1 = START_X + source_x * CELL_X + 40
            y1 = START_Y + source_y * CELL_Y + 20
            x2 = START_X + target_x * CELL_X + 0
            y2 = START_Y + target_y * CELL_Y + 20
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref,
                    ref2=source_activity['ID'],
                    ref3=target_activity['ID'],
                    color=processgroup['Color'],
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
        elif source_x < target_x and source_y < target_y:
            x1 = START_X + source_x * CELL_X + 30
            y1 = START_Y + source_y * CELL_Y + 0
            x2 = START_X + target_x * CELL_X + 0
            y2 = START_Y + target_y * CELL_Y + 0
            if routing > 1:
                result.append(
                    DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                        ref1=ref + 6,
                        ref2=source_activity['ID'],
                        ref3=ref,
                        color=processgroup['Color'],
                        exit_x=1,
                        exit_y=0.5,
                        entry_x=0,
                        entry_y=0.5,
                        x1=x1,
                        x2=x1 + CELL_X * (routing - 1),
                        y1=y1,
                        y2=y1
                    )
                )
                x1 += CELL_X * (routing - 1)

            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_LU.format(
                    ref1=ref,
                    ref2=ref + 1,
                    color=processgroup['Color'],
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
                    ref1=ref + 2,
                    ref2=ref + 3,
                    color=processgroup['Color'],
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
                    ref1=ref + 4,
                    ref2=ref,
                    ref3=ref + 2,
                    color=processgroup['Color'],
                    exit_x=0.5,
                    exit_y=1,
                    entry_x=0.5,
                    entry_y=0,
                    x1=x1 + 40,
                    x2=x1 + 40,
                    y1=y1 + CELL_Y,
                    y2=y2 - 80
                )
            )
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref + 5,
                    ref2=ref + 2,
                    ref3=target_activity['ID'],
                    color=processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0,
                    entry_y=0.5,
                    x1=x1 + CELL_X,
                    x2=x2,
                    y1=y2,
                    y2=y2
                )
            )
        elif source_x < target_x and source_y > target_y:
            x1 = START_X + source_x * CELL_X + 30
            y1 = START_Y + source_y * CELL_Y + 0
            x2 = START_X + target_x * CELL_X + 0
            y2 = START_Y + target_y * CELL_Y + 0
            if routing > 1:
                result.append(
                    DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                        ref1=ref + 6,
                        ref2=source_activity['ID'],
                        ref3=ref,
                        color=processgroup['Color'],
                        exit_x=1,
                        exit_y=0.5,
                        entry_x=0,
                        entry_y=0.5,
                        x1=x1,
                        x2=x1 + CELL_X * (routing - 1),
                        y1=y1,
                        y2=y1
                    )
                )
                x1 += CELL_X * (routing - 1)
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_LO.format(
                    ref1=ref,
                    ref2=ref + 1,
                    color=processgroup['Color'],
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
                    ref1=ref + 2,
                    ref2=ref + 3,
                    color=processgroup['Color'],
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
                    ref1=ref + 4,
                    ref2=ref,
                    ref3=ref + 2,
                    color=processgroup['Color'],
                    exit_x=0.5,
                    exit_y=0,
                    entry_x=0.5,
                    entry_y=1,
                    x1=x1 + 40,
                    x2=x1 + 40,
                    y1=y1 - CELL_Y,
                    y2=y2 + 80
                )
            )
            result.append(
                DRAWIO_XML_TEMPLATE_CONNECTION_STRAIGHT.format(
                    ref1=ref + 5,
                    ref2=ref + 2,
                    ref3=target_id,
                    color=processgroup['Color'],
                    exit_x=1,
                    exit_y=0.5,
                    entry_x=0,
                    entry_y=0.5,
                    x1=x1 + CELL_X,
                    x2=x2,
                    y1=y2,
                    y2=y2
                )
            )

        ref += 7

    return ''.join(result)

def add_activities(activities: list[dict[str, str]], process_groups: list[dict[str, str]], START_X: int, START_Y: int) -> str:
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

def get_max_activity_x_for_phase(activities: list[dict[str, str]], phase: str) -> int:
    """Return the maximum X position for activities in the given phase.
    
    Returns 0 if no matching activities are found.
    """
    phase_x_values = [
        int(activity.get('X', 0))
        for activity in activities
        if str(activity.get('Phase', '')).strip() == phase
    ]
    return max(phase_x_values, default=0)

def get_max_activity_row(activities: list[dict[str, str]]) -> int:
    """Return the maximum Y position from the given activities list.
    
    Returns 0 if activities list is empty.
    """
    if not activities:
        return 0
    return max(int(activity.get('Y', 0)) for activity in activities)

def add_activities_layer(activityconnections: list[dict[str, str]], activities: list[dict[str, str]], process_groups: list[dict[str, str]], START_X: int, START_Y: int) -> str:
    result: list[str] = []
    result.append(DRAWIO_XML_TEMPLATE_ACTIVITIES_LAYER)
    result.append(add_activityconnections(activityconnections, activities, process_groups, START_X, START_Y))
    result.append(add_activities(activities, process_groups, START_X, START_Y))
    return ''.join(result)
