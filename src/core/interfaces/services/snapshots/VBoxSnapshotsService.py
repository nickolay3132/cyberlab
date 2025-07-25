from abc import ABC, abstractmethod

from src.core.entities.VirtualMachine import VirtualMachine
from src.core.entities.observer import Subject


class VBoxSnapshotsService(ABC):
    @abstractmethod
    def create_snapshot_for_all(self, subject: Subject, snapshot_name: str, description: str = '') -> None: pass

    @abstractmethod
    def list_snapshots(self, subject: Subject) -> None: pass

    @abstractmethod
    def restore_snapshot(self, name: str, subject: Subject) -> None: pass