import re
from dataclasses import dataclass, field
from typing import List

from src.core.entities.Snapshot import Snapshot
from src.core.interfaces.services.snapshots.SnapshotsTreeService import SnapshotsTreeService

@dataclass
class SnapshotsTreeServiceImpl(SnapshotsTreeService):
    root_nodes: List[Snapshot] = field(init=False, default_factory=list)

    def get_tree_data(self) -> List[Snapshot]:
        return self.root_nodes

    def get_flat_list(self) -> List[Snapshot]:
        flat_list = []
        stack = list(self.root_nodes)

        while stack:
            node = stack.pop()
            children = node.children
            node.children = []
            flat_list.append(node)
            stack.extend(reversed(children))

        return flat_list

    def parse_output(self, text: str) -> None:
        self.root_nodes = []
        parent_stack = []
        indent_stack = []

        for line in text.split('\n'):
            if not line.strip():
                continue

            indent = len(line) - len(line.lstrip())

            if 'Name:' in line:
                name = re.sub(r'^\d+-', '', re.search(r'Name: (.+?) \(UUID:', line).group(1))
                is_current = '*' in line

                timestamp_match = re.match(r'^(\d+)', re.search(r'Name: (.+?) \(UUID:', line).group(1))
                timestamp = int(timestamp_match.group(1)) if timestamp_match else 0

                while parent_stack and indent_stack[-1] >= indent:
                    parent_stack.pop()
                    indent_stack.pop()

                node = Snapshot(
                    name=name,
                    description='',
                    timestamp=timestamp,
                    is_current=is_current,
                    children=[]
                )

                if parent_stack:
                    parent_stack[-1].children.append(node)
                else:
                    self.root_nodes.append(node)

                parent_stack.append(node)
                indent_stack.append(indent)

            elif 'Description:' in line and parent_stack:
                desc = line.split('Description:', 1)[1].strip()
                if desc:
                    parent_stack[-1].description = desc