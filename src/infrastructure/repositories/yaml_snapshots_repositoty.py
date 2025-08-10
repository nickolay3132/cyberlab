from typing import Optional, List

from src.core.entities import Snapshot
from src.core.interfaces.repositories import ISnapshotsRepository
from src.infrastructure.repositories import YamlLoader


def recursive(func):
    func._is_recursive = True
    func.__doc__ = (func.__doc__ or "") + "\n\nNote: This function is recursive."
    return func

@recursive
def _find_current(root: Snapshot) -> Optional[Snapshot]:
    if root.is_current:
        return root
    for child in root.children:
        found = _find_current(child)
        if found:
            return found
    return None

@recursive
def _find_by_identity(root: Snapshot, name: str, timestamp: int) -> Optional[Snapshot]:
    if root.name == name and root.timestamp == timestamp:
        return root
    for child in root.children:
        found = _find_by_identity(child, name, timestamp)
        if found:
            return found
    return None

@recursive
def _find_all_by_name(root: Snapshot, name: str) -> List[Snapshot]:
    result = []
    if root.name == name:
        result.append(root)
    for child in root.children:
        result.extend(_find_all_by_name(child, name))
    return result

@recursive
def _mark_all_non_current(root: Optional[Snapshot]) -> None:
    if not root:
        return

    root.is_current = False
    for child in root.children:
        _mark_all_non_current(child)


class YamlSnapshotRepository(ISnapshotsRepository):
    def __init__(self, yaml_loader: YamlLoader):
        self.yaml_loader = yaml_loader
        self.root_snapshot = self._load()

    def _load(self) -> Optional[Snapshot]:
        data = self.yaml_loader.read(create_if_not_exists=True)
        return Snapshot.from_dict(data) if data else None

    def _save(self) -> None:
        self.yaml_loader.write(self.root_snapshot.to_dict() if self.root_snapshot else {})

    def add_snapshot(self, snapshot: Snapshot, parent_snapshot: Optional[Snapshot]) -> bool:
        self.root_snapshot = self._load()

        # Skip if root exists and an identical snapshot (by name and timestamp) is already present
        if self.root_snapshot:
            existing = _find_by_identity(self.root_snapshot, snapshot.name, snapshot.timestamp)
            if existing:
                return False

        _mark_all_non_current(self.root_snapshot)
        snapshot.is_current = True

        if parent_snapshot is None:
            if self.root_snapshot:
                snapshot.children.append(self.root_snapshot)
            self.root_snapshot = snapshot
        else:
            parent = _find_by_identity(self.root_snapshot, parent_snapshot.name, parent_snapshot.timestamp)
            if not parent:
                return False
            parent.children.append(snapshot)

        self._save()
        return True

    def get_current_snapshot(self) -> Optional[Snapshot]:
        self.root_snapshot = self._load()
        return _find_current(self.root_snapshot) if self.root_snapshot else None

    def find_snapshot(self, name: str) -> Optional[Snapshot]:
        self.root_snapshot = self._load()
        if not self.root_snapshot:
            return None
        snapshots = _find_all_by_name(self.root_snapshot, name)
        return max(snapshots, key=lambda s: s.timestamp, default=None)

    def find_all_snapshots(self, name: str) -> List[Snapshot]:
        self.root_snapshot = self._load()
        return _find_all_by_name(self.root_snapshot, name) if self.root_snapshot else []

    def get_root_snapshot(self) -> Optional[Snapshot]:
        self.root_snapshot = self._load()
        return self.root_snapshot

    def restore_snapshot(self, snapshot: Snapshot) -> bool:
        self.root_snapshot = self._load()
        if not self.root_snapshot:
            return False

        target = _find_by_identity(self.root_snapshot, snapshot.name, snapshot.timestamp)
        if not target:
            return False

        _mark_all_non_current(self.root_snapshot)
        target.is_current = True
        self._save()
        return True

    def _find_latest_by_name(self, name: str) -> Optional[Snapshot]:
        snapshots = _find_all_by_name(self.root_snapshot, name)
        return max(snapshots, key=lambda s: s.timestamp, default=None)

