from abc import ABC, abstractmethod
from typing import List

from src.core.entities import VM


class IVMRepository(ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> VM: pass

    @abstractmethod
    def get_all(self) -> List[VM]: pass