from abc import ABC, abstractmethod

from src.core.entities import VM


class IVmNetworkService(ABC):
    @abstractmethod
    def enable_vm_nics(self, vm: VM) -> bool: pass