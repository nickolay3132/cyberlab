from abc import ABC, abstractmethod

from src.core.entities import VM, Snapshot


class IVmsSnapshotsGateway(ABC):
    @abstractmethod
    def create_snapshot(self, vm: VM, snapshot: Snapshot) -> bool: pass

    @abstractmethod
    def restore_snapshot(self, vm: VM, snapshot: Snapshot) -> bool: pass