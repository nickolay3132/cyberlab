from abc import ABC, abstractmethod
from typing import List, Callable

from src.core.entities import VM, Snapshot


class IVmSnapshotsService(ABC):
    @abstractmethod
    def create_snapshot(self, vm: VM, snapshot: Snapshot) -> bool: pass

    @abstractmethod
    def restore_snapshot(self, vm: VM, snapshot: Snapshot) -> bool: pass