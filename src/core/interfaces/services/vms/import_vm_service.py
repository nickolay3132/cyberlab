from abc import ABC, abstractmethod
from typing import Callable, Tuple

from src.core.entities import VM


class IImportVMService(ABC):
    @abstractmethod
    def set_callback(self, callback: Callable[[str, bool], None]) -> None: pass

    @abstractmethod
    def prepare_storage(self, vms_store_to: str, log_store_to: str) -> Tuple[str, str]: pass

    @abstractmethod
    def import_vm(self, vm: VM, ova_dir: str, log_dir: str) -> None: pass