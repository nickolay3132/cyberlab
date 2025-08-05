from abc import ABC, abstractmethod
from typing import Optional, Callable

from src.core.enums import DownloadingType


class IFileSystemService(ABC):
    @abstractmethod
    def download_file(self,
                      url: str,
                      download_path: str,
                      callback: Callable[[DownloadingType, int, int, Optional[str]], None]
                      ) -> bool: pass

    @abstractmethod
    def mkdirs(self, *paths: str) -> None: pass

    @abstractmethod
    def file_exists(self, path: str) -> bool: pass

    @abstractmethod
    def to_absolute_path(self, path: str) -> str: pass

    @abstractmethod
    def calc_md5(self, file_path: str) -> str: pass

