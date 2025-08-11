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
    stack = [root]
    while stack:
        node = stack.pop()
        if node.is_current:
            return node
        stack.extend(reversed(node.children))
    return None

@recursive
def _find_by_identity(root: Snapshot, name: str, timestamp: int) -> Optional[Snapshot]:
    stack = [root]
    while stack:
        node = stack.pop()
        if node.name == name and node.timestamp == timestamp:
            return node
        stack.extend(reversed(node.children))
    return None

@recursive
def _find_all_by_name(root: Snapshot, name: str) -> List[Snapshot]:
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node.name == name:
            result.append(node)
        stack.extend(reversed(node.children))
    return result

@recursive
def _mark_all_non_current(root: Optional[Snapshot]) -> None:
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        node.is_current = False
        stack.extend(reversed(node.children))


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

    # def find_snapshot(self, target: Snapshot) -> Optional[Snapshot]:
    #     self.root_snapshot = self._load()
    #     if not self.root_snapshot:
    #         return None
    #     return _find_by_identity(self.root_snapshot, target.name, target.timestamp)

    def find_all_snapshots(self, name: str) -> List[Snapshot]:
        self.root_snapshot = self._load()
        return _find_all_by_name(self.root_snapshot, name) if self.root_snapshot else []

    def find_by_identity(self, name: str, timestamp: int) -> Optional[Snapshot]:
        return _find_by_identity(self.root_snapshot, name, timestamp) if self.root_snapshot else None

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

