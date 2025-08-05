from abc import ABC, abstractmethod
from typing import Tuple, Callable, Optional

from src.core.enums import DownloadingType


class IInstallVMService(ABC):
    @abstractmethod
    def set_no_verify_checksum(self, no_verify_checksum: bool) -> None: pass

    @abstractmethod
    def set_callback(self, callback: Callable[[DownloadingType, int, int, Optional[str]], None]) -> None: pass

    @abstractmethod
    def prepare_storage(self, ova_store_to: str) -> str: pass

    @abstractmethod
    def install(self, ova_url: str, download_path: str, md5checksum: str) -> bool: pass