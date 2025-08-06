from abc import ABC, abstractmethod

from src.core.enums import BootPolicyStartupType, BootPolicyShutdownType


class IVmBootService(ABC):
    @abstractmethod
    def startup(self, vm_name: str, startup_boot_policy: BootPolicyStartupType) -> bool: pass

    @abstractmethod
    def shutdown(self, vm_name: str, startup_boot_policy: BootPolicyShutdownType, force: bool = False) -> bool: pass