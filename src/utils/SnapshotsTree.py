from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from colorama.ansi import Fore

@dataclass
class SnapshotData:
    name: str
    description: str
    timestamp: int
    is_current: bool
    indent: int
    children: List[SnapshotData]

class SnapshotsTree:
    def __init__(self, vbox_output):
        self.snapshots = []
        self._parse_vbox_output(vbox_output)

    def _parse_vbox_output(self, text):
        parent_stack = []

        for line in text.split('\n'):
            if not line.strip():
                continue

            indent = len(line) - len(line.lstrip())

            if 'Name:' in line:
                name = re.sub(r'^\d+-', '', re.search(r'Name: (.+?) \(UUID:', line).group(1))
                is_current = '*' in line

                timestamp_match = re.match(r'^(\d+)', re.search(r'Name: (.+?) \(UUID:', line).group(1))
                timestamp = int(timestamp_match.group(1)) if timestamp_match else 0

                while parent_stack and parent_stack[-1].indent >= indent:
                    parent_stack.pop()

                snapshot = SnapshotData(
                    name=name,
                    description='',
                    timestamp=timestamp,
                    is_current=is_current,
                    indent=indent,
                    children=[]
                )

                if parent_stack:
                    parent_stack[-1].children.append(snapshot)
                else:
                    self.snapshots.append(snapshot)

                parent_stack.append(snapshot)

            elif 'Description:' in line and parent_stack:
                desc = line.split('Description:', 1)[1].strip()
                if desc:
                    parent_stack[-1].description = desc

    def _format_recursive(self, nodes: List[SnapshotData], level=0):
        result = []
        for node in nodes:
            indent = '    ' * level
            line = f"{indent}{node.name} ({node.description})"
            if node.is_current:
                line += f" {Fore.GREEN}<- current state"
            result.append(line)
            result.extend(self._format_recursive(node.children, level + 1))
        return result

    def get_formatted(self):
        return self._format_recursive(self.snapshots)

    def get_list(self):
        flat_list = []
        stack = list(self.snapshots)

        while stack:
            node = stack.pop()
            children = node.children
            node.children = []
            flat_list.append(node)
            stack.extend(reversed(children))

        return flat_list

    def print(self):
        for line in self.get_formatted():
            print(line)