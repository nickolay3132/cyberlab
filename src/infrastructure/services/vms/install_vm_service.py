import os
import time
from typing import Callable, Optional

from src.core.enums import DownloadingType
from src.core.interfaces.services import IFileSystemService
from src.core.interfaces.services.vms import IInstallVMService


class InstallVMServiceImpl(IInstallVMService):
    def __init__(self, file_system_service: IFileSystemService) -> None:
        self.file_system_service = file_system_service

        self.no_verify_checksum = False
        self.callback = lambda _, __, ___, ____: None

    def set_no_verify_checksum(self, no_verify_checksum: bool) -> None:
        self.no_verify_checksum = no_verify_checksum

    def set_callback(self, callback: Callable[[DownloadingType, int, int, Optional[str]], None]) -> None:
        self.callback = callback

    def prepare_storage(self, ova_store_to: str) -> str:
        absolute_ova_path = self.file_system_service.to_absolute_path(ova_store_to)
        self.file_system_service.mkdirs(absolute_ova_path)
        return absolute_ova_path

    def install(self, ova_url: str, download_path: str, md5checksum: str) -> bool:
        download_needed = self._is_download_needed(md5checksum, download_path)

        if download_needed:
            time.sleep(0.5)
            self.file_system_service.download_file(ova_url, download_path, self.callback)
            return True
        else:
            return False

    def _is_download_needed(self, md5checksum: str, download_path: str) -> bool:
        if not os.path.exists(download_path):
            return True
        else:
            if not self.no_verify_checksum:
                if md5checksum != self.file_system_service.calc_md5(download_path):
                    return True

        return False