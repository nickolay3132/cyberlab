from abc import ABC, abstractmethod
from typing import Optional, List

from src.core.entities.Snapshot import Snapshot


class SnapshotsRepository(ABC):
    @abstractmethod
    def add_snapshot(self, snapshot: Snapshot, parent_name: Optional[str] = None) -> bool: pass

    @abstractmethod
    def get_current_snapshot(self) -> Optional[Snapshot]: pass

    @abstractmethod
    def find_snapshot(self, name: str) -> Optional[Snapshot]: pass

    @abstractmethod
    def find_all_snapshots(self, name: str) -> List[Snapshot]: pass

    @abstractmethod
    def get_root_snapshot(self) -> Optional[Snapshot]: pass

    @abstractmethod
    def get_snapshots_as_list(self) -> List[Snapshot]: pass

    @abstractmethod
    def restore_snapshot(self, snapshot: Snapshot) -> bool: pass
