from typing import List

from colorama.ansi import Fore

from src.core.entities.Snapshot import Snapshot
from src.core.entities.observer import ObserverEvent
from src.presentation.cli.observers.cli_observer_invoker import CLIObserverInvoker


class SnapshotTreeCLIObserver(CLIObserverInvoker):
    def __init__(self):
        super().__init__()

        self.add_event_handlers({
            'display_snapshot_tree': self.display_snapshots_tree_event
        })

    def display_snapshots_tree_event(self, event: ObserverEvent):
        formatted_snapshots = self._format_snapshots_tree([event.data])

        for line in formatted_snapshots:
            print(line)

    def _format_snapshots_tree(self, nodes: List[Snapshot], level=0):
        result = []
        for node in nodes:
            indent = '    ' * level
            line = f"{indent}{node.name} ({node.description})"
            if node.is_current:
                line += f" {Fore.GREEN}<- current snapshot"
            result.append(line)
            result.extend(self._format_snapshots_tree(node.children, level + 1))
        return result