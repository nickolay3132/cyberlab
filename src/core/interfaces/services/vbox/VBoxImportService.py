from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.core.entities.VirtualMachine import VirtualMachine

@dataclass
class ImportVMsDTO:
    vms: List[VirtualMachine]
    log_dir: str
    vms_dir: str
    ova_dir: str

class VBoxImportService(ABC):
    @abstractmethod
    def import_vms(self, dto: ImportVMsDTO) -> None: pass
