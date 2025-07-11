from abc import ABC, abstractmethod

from src.core.entities.VirtualMachine import VirtualMachine


class VBoxSnapshotService(ABC):
    @abstractmethod
    def create_snapshot(self, vm: VirtualMachine, snapshot_name: str, description: str = '') -> None: pass

    @abstractmethod
    def create_snapshot_for_all(self, snapshot_name: str, description: str = '') -> None: pass