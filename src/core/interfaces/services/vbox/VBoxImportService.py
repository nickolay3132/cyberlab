from abc import ABC, abstractmethod

from src.core.entities.observer import Subject


class VBoxImportService(ABC):
    @abstractmethod
    def import_vms(self, subject: Subject) -> None: pass
