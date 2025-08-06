from abc import ABC, abstractmethod


class IVMsGateway(ABC):
    @abstractmethod
    def import_vm(self, ova_path: str, vm_name: str, vms_dir: str, log_file) -> int: pass