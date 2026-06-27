#!/usr/bin/env python3
"""Generate Draw.io XML for process groups from YAML input."""

from __future__ import annotations
from typing import Any

DRAWIO_XML_TEMPLATE_PROCESSGROUPS = '''
                <mxCell id="re-hWYANieQfaZoZakJm-{ref1}" value="{group}" style="html=1;whiteSpace=wrap;fontSize=11;fontColor=#000000;align=left;spacing=0;verticalAlign=middle;strokeOpacity=100;fillOpacity=100;fillColor=none;strokeWidth=3.6;strokeColor=none;" vertex="1" parent="re-hWYANieQfaZoZakJm-001">
                    <mxGeometry x="113" y="{ypos1}" width="150" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-{ref2}" value="" style="html=1;whiteSpace=wrap;;fontSize=11;align=center;spacingTop=9;spacing=5;verticalAlign=bottom;strokeOpacity=0;fillOpacity=100;rounded=1;absoluteArcSize=1;arcSize=109.2;fillColor={color};strokeWidth=0.6;strokeColor={color};" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="55" y="{ypos2}" width="25" height="25" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-{ref3}" value="" style="html=1;whiteSpace=wrap;;fontSize=11;align=center;spacingTop=9;spacing=5;verticalAlign=bottom;strokeOpacity=0;fillOpacity=100;rounded=1;absoluteArcSize=1;arcSize=109.2;fillColor=#ffffff;strokeWidth=0.6;strokeColor={color};" parent="re-hWYANieQfaZoZakJm-001" vertex="1">
                    <mxGeometry x="62" y="{ypos3}" width="12.5" height="12.5" as="geometry"/>
                </mxCell>
                <mxCell id="re-hWYANieQfaZoZakJm-{ref4}" value="" style="html=1;jettySize=18;fontSize=11;strokeColor={color};strokeOpacity=100;strokeWidth=6;rounded=1;arcSize=0;startArrow=none;endArrow=none;" parent="re-hWYANieQfaZoZakJm-001" edge="1">
                    <mxGeometry width="100" height="100" relative="1" as="geometry">
                        <mxPoint x="77" y="{ypos4}" as="sourcePoint"/>
                        <mxPoint x="96" y="{ypos4}" as="targetPoint"/>
                    </mxGeometry>
                </mxCell>
'''

def add_process_group_layer(process_groups: list[dict[str, str]]) -> str:
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

            name = str(normalized['name'])
            color = str(normalized.get('color', ''))
        else:
            raise ValueError('Each ProcessGroups item must be a string or mapping with a Name key')

        process_groups.append({'Name': name, 'Color': color})
    return process_groups

def count_process_groups(process_groups: list[dict[str, str]]) -> int:
    """Return the number of process groups."""
    return len(process_groups)
