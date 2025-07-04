import datetime
import sys
from typing import List, Tuple, Dict, Optional

from colorama.ansi import Fore, Style

from src.utils.SnapshotsTree import SnapshotData


class SnapshotSelector:
    def __init__(self, all_snapshots: Dict[str, List['SnapshotData']]):
        self.all_snapshots = all_snapshots
        self.selected_snapshot = None

    def find_snapshots_by_name(self, target_name: str) -> List[Tuple[str, SnapshotData]]:
        candidates = []
        for vm_name, snapshots in self.all_snapshots.items():
            for snap in snapshots:
                if snap.name == target_name:
                    candidates.append((vm_name, snap))
        return candidates

    @staticmethod
    def get_unique_snapshots(snapshots: List[Tuple[str, SnapshotData]]) -> Dict[Tuple[int, str], SnapshotData]:
        unique = {}
        for _, snap in snapshots:
            key = (snap.timestamp, snap.name)
            if key not in unique:
                unique[key] = snap
        return unique

    @staticmethod
    def prompt_user_selection(unique_snapshots: Dict[Tuple[int, str], SnapshotData]) -> SnapshotData:
        print(f"{Fore.CYAN}Found {len(unique_snapshots)} variants of snapshots:")
        for i, ((timestamp, name), snap) in enumerate(unique_snapshots.items(), 1):
            date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{i}) {date_str} {name} ({snap.description})")

        while True:
            try:
                choice = int(input(f"{Fore.CYAN}Select snapshot number: {Style.RESET_ALL}"))
                if 1 <= choice <= len(unique_snapshots):
                    return list(unique_snapshots.values())[choice - 1]
                print(f"{Fore.RED}Invalid number. Try again.")
            except ValueError:
                print(f"{Fore.RED}Enter a number.")

    def select_for_all_vms(self, target_snapshot_name: str) -> Dict[str, Optional[SnapshotData]]:
        candidates = self.find_snapshots_by_name(target_snapshot_name)

        if not candidates:
            print(f"{Fore.RED}Snapshot '{target_snapshot_name}' not found in any VM")
            sys.exit(1)

        unique_snapshots = self.get_unique_snapshots(candidates)

        if len(unique_snapshots) > 1:
            self.selected_snapshot = self.prompt_user_selection(unique_snapshots)
        else:
            self.selected_snapshot = next(iter(unique_snapshots.values()))

        result = {}
        for vm_name, snapshots in self.all_snapshots.items():
            result[vm_name] = next(
                (s for s in snapshots
                 if s.name == self.selected_snapshot.name
                 and s.timestamp == self.selected_snapshot.timestamp),
                None
            )

        return result