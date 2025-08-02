from abc import ABC, abstractmethod
from typing import List

from src.core.entities.VirtualMachine import VirtualMachine


class VirtualMachinesInstallerService (ABC):
    @abstractmethod
    def install(self, no_verify_checksum: bool = False) -> List[VirtualMachine]: pass