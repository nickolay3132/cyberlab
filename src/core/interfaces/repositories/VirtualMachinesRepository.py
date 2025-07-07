from abc import ABC, abstractmethod
from typing import List

from src.core.entities.VirtualMachine import VirtualMachine


class VirtualMachinesRepository (ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> VirtualMachine: pass

    @abstractmethod
    def get_all(self) -> List[VirtualMachine]: pass