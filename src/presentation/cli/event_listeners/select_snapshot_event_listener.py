from datetime import datetime

from src.core.entities.event_bus.events import SelectSnapshotEvent


GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'

def format_timestamp(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def select_snapshot_event_listener(event: SelectSnapshotEvent):
    snapshots = event.snapshots
    if not snapshots:
        print("No snapshots to select.")
        return

    for idx, snapshot in enumerate(snapshots):
        label = f"{format_timestamp(snapshot.timestamp)} - {snapshot.name} ({snapshot.description})"
        if snapshot.is_current:
            label = f"{GREEN}{label} <- current snapshot{RESET}"
        print(f"{idx + 1} {label}")

    while True:
        user_input = input("Select snapshot by index: ").strip()
        if not user_input.isdigit():
            print(f"{YELLOW}Invalid input. Please enter a number.{RESET}")
            continue

        selected_index = int(user_input) - 1
        if 0 <= selected_index < len(snapshots):
            selected_snapshot = snapshots[selected_index]
            event.callback(selected_snapshot)
            break
        else:
            print(f"{YELLOW}Index out of range. Try again.{RESET}")