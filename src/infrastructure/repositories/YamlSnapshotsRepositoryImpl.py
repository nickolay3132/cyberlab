from dataclasses import dataclass
from typing import Optional, List

from src.core.entities.Snapshot import Snapshot
from src.core.interfaces.repositories.SnapshotsRepository import SnapshotsRepository
from src.infrastructure.repositories.common.YamlLoader import YamlLoader


class YamlSnapshotsRepositoryImpl(SnapshotsRepository):
    def __init__(self, yaml_loader: YamlLoader):
        self.yaml_loader = yaml_loader
        self.root_snapshot = self._load_snapshots()

    def _load_snapshots(self) -> Optional[Snapshot]:
        data = self.yaml_loader.reread(create_if_not_exists=True)
        if not data:
            return None
        return Snapshot.from_dict(data)

    def add_snapshot(self, snapshot: Snapshot, parent_name: Optional[str] = None) -> bool:
        self.root_snapshot = self._load_snapshots()

        if self._snapshot_exists(snapshot.name, snapshot.timestamp):
            return False

        if parent_name is None:
            snapshot.is_current = True
            self._mark_all_non_current(self.root_snapshot)
            if self.root_snapshot is None:
                self.root_snapshot = snapshot
            else:
                snapshot.children.append(self.root_snapshot)
                self.root_snapshot = snapshot
        else:
            parent = self.find_snapshot(parent_name)
            if not parent:
                return False

            snapshot.is_current = True
            self._mark_all_non_current(self.root_snapshot)
            parent.children.append(snapshot)

        self._save()
        return True

    def get_current_snapshot(self) -> Optional[Snapshot]:
        self.root_snapshot = self._load_snapshots()

        if self.root_snapshot is None:
            return None
        return self._find_current(self.root_snapshot)

    def find_snapshot(self, name: str) -> Optional[Snapshot]:
        self.root_snapshot = self._load_snapshots()

        if self.root_snapshot is None:
            return None
        return self._find_by_name(self.root_snapshot, name)

    def find_all_snapshots(self, name: str) -> List[Snapshot]:
        self.root_snapshot = self._load_snapshots()

        if self.root_snapshot is None:
            return []

        return self._find_all_by_name(self.root_snapshot, name)


    def get_root_snapshot(self) -> Optional[Snapshot]:
        self.root_snapshot = self._load_snapshots()

        return self.root_snapshot

    def get_snapshots_as_list(self) -> List[Snapshot]:
        self.root_snapshot = self._load_snapshots()

        if self.root_snapshot is None:
            return []

        flat_list: List[Snapshot] = []
        stack: List[Snapshot] = [self.root_snapshot]

        while stack:
            current = stack.pop()
            snapshot_copy = Snapshot(
                name=current.name,
                description=current.description,
                timestamp=current.timestamp,
                is_current=current.is_current,
                children=[]
            )
            flat_list.append(snapshot_copy)
            stack.extend(reversed(current.children))

        return flat_list

    def restore_snapshot(self, snapshot: Snapshot) -> bool:
        self.root_snapshot = self._load_snapshots()

        if self.root_snapshot is None:
            return False

        snapshot_names = [f"{s.timestamp}-{s.name}" for s in self.get_snapshots_as_list()]
        if f"{snapshot.timestamp}-{snapshot.name}" not in snapshot_names:
            return False

        self._mark_all_non_current(self.root_snapshot)

        snapshot.is_current = True

        self._save()
        return True

    def _mark_all_non_current(self, snapshot: Optional[Snapshot]) -> None:
        if snapshot is None:
            return
        snapshot.is_current = False
        for child in snapshot.children:
            self._mark_all_non_current(child)

    def _find_current(self, snapshot: Snapshot) -> Optional[Snapshot]:
        if snapshot.is_current:
            return snapshot
        for child in snapshot.children:
            found = self._find_current(child)
            if found:
                return found
        return None

    def _find_by_name(self, snapshot: Snapshot, name: str) -> Optional[Snapshot]:
        if snapshot.name == name:
            return snapshot
        for child in snapshot.children:
            found = self._find_by_name(child, name)
            if found:
                return found
        return None

    def _find_all_by_name(self, snapshot: Snapshot, name: str) -> List[Snapshot]:
        result = []

        if snapshot.name == name:
            result.append(snapshot)

        for child in snapshot.children:
            result.extend(self._find_all_by_name(child, name))

        return result

    def _save(self) -> None:
        if self.root_snapshot is None:
            self.yaml_loader.write({})
        else:
            self.yaml_loader.write(self.root_snapshot.to_dict())

    def _snapshot_exists(self, name: str, timestamp: int) -> bool:
        if self.root_snapshot is None:
            return False
        return self._check_snapshot_exists(self.root_snapshot, name, timestamp)

    def _check_snapshot_exists(self, snapshot: Snapshot, name: str, timestamp: int) -> bool:
        if snapshot.name == name and snapshot.timestamp == timestamp:
            return True

        for child in snapshot.children:
            if self._check_snapshot_exists(child, name, timestamp):
                return True

        return False