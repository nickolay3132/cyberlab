from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities.VirtualMachine import VirtualMachine


class VBoxImportService(ABC):
    @abstractmethod
    def import_vms(self, reimport: Optional[List[VirtualMachine]]) -> None: pass
