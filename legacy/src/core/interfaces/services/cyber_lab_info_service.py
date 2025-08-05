from abc import ABC, abstractmethod

from src.core.entities.VirtualMachine import VirtualMachine


class CyberLabInfoService(ABC):
    @abstractmethod
    def is_installed(self, vm: VirtualMachine) -> bool: pass

    @abstractmethod
    def is_running(self, vm: VirtualMachine) -> bool: pass