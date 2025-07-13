from abc import ABC, abstractmethod

from src.core.entities.VirtualMachine import VirtualMachine


class VBoxSnapshotsService(ABC):
    @abstractmethod
    def create_snapshot_for_all(self, snapshot_name: str, description: str = '') -> None: pass

    @abstractmethod
    def list_snapshots(self) -> None: pass

    @abstractmethod
    def restore_snapshot(self, name: str) -> None: pass