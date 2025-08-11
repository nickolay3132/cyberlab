from abc import ABC, abstractmethod

from src.core.entities import VM


class IVMsGateway(ABC):
    @abstractmethod
    def import_vm(self, ova_path: str, vm_name: str, vms_dir: str, log_file) -> int: pass

    @abstractmethod
    def is_running(self, vm: VM) -> bool: pass