from abc import ABC, abstractmethod
from typing import Optional, List

from src.core.entities import Snapshot


class ISnapshotsRepository(ABC):
    @abstractmethod
    def add_snapshot(self, snapshot: Snapshot, parent_snapshot: Optional[Snapshot]) -> bool: pass

    @abstractmethod
    def get_current_snapshot(self) -> Optional[Snapshot]: pass

    # @abstractmethod
    # def find_snapshot(self, target: Snapshot) -> Optional[Snapshot]: pass

    @abstractmethod
    def find_all_snapshots(self, name: str) -> List[Snapshot]: pass

    @abstractmethod
    def get_root_snapshot(self) -> Optional[Snapshot]: pass

    @abstractmethod
    def restore_snapshot(self, snapshot: Snapshot) -> bool: pass