from abc import ABC, abstractmethod


class VBoxImportService(ABC):
    @abstractmethod
    def import_vms(self) -> None: pass
