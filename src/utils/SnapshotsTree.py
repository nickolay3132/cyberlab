import re

from colorama.ansi import Fore


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

                while parent_stack and parent_stack[-1]['indent'] >= indent:
                    parent_stack.pop()

                snapshot = {
                    'name': name,
                    'description': '',
                    'is_current': is_current,
                    'indent': indent,
                    'children': []
                }

                if parent_stack:
                    parent_stack[-1]['children'].append(snapshot)
                else:
                    self.snapshots.append(snapshot)

                parent_stack.append(snapshot)

            elif 'Description:' in line and parent_stack:
                desc = line.split('Description:', 1)[1].strip()
                if desc:
                    parent_stack[-1]['description'] = desc

    def _format_recursive(self, nodes, level=0):
        result = []
        for node in nodes:
            indent = '    ' * level
            line = f"{indent}{node['name']} ({node['description']})"
            if node['is_current']:
                line += f" {Fore.GREEN}<- current state"
            result.append(line)
            result.extend(self._format_recursive(node['children'], level + 1))
        return result

    def get_formatted(self):
        return self._format_recursive(self.snapshots)

    def print(self):
        for line in self.get_formatted():
            print(line)