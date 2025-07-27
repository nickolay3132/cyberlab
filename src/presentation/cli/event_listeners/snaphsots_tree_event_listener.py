from typing import List

from colorama.ansi import Fore

from src.core.entities.Snapshot import Snapshot
from src.core.entities.event_bus import EventListener
from src.core.entities.event_bus.events import SnapshotsTreeEvent


class SnapshotsTreeEventListener(EventListener[SnapshotsTreeEvent]):
    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        pass

    def on_event(self, event: SnapshotsTreeEvent) -> None:
        formatted_snapshots = self._format_snapshots_tree([event.root_snapshot])

        for line in formatted_snapshots:
            print(line)

    def _format_snapshots_tree(self, nodes: List[Snapshot], level=0):
        result = []
        for node in nodes:
            indent = '    ' * level
            line = f"{indent}{node.name}"
            if node.description != '':
                line += f" ({node.description})"

            if node.is_current:
                line += f" {Fore.GREEN}<- current snapshot"
            result.append(line)
            result.extend(self._format_snapshots_tree(node.children, level + 1))
        return result