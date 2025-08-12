from datetime import datetime

from src.core.entities.event_bus.events import SnapshotsTreeEvent

GREEN = '\033[32m'
RESET = '\033[0m'

def format_timestamp(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def snapshots_tree_event_listener(event: SnapshotsTreeEvent):
    if event.root_snapshot is None:
        print("No snapshots available.")
        return

    stack = [(event.root_snapshot, "", False)]  # (snapshot, prefix, is_last)

    while stack:
        snapshot, prefix, is_last = stack.pop()

        connector = "|-- "
        line = f"{format_timestamp(snapshot.timestamp)} - {snapshot.name} ({snapshot.description})"
        if snapshot.is_current:
            line = f"{GREEN}{line}{RESET}"
        print(f"{prefix}{connector}{line}" if prefix else line)

        # Построим префикс для детей
        child_prefix = prefix + ("    " if is_last else "|   ")

        # Добавим детей в стек в обратном порядке
        children = snapshot.children
        for i in reversed(range(len(children))):
            child = children[i]
            stack.append((child, child_prefix, i == len(children) - 1))