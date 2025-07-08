import os
from typing import Optional
from urllib.parse import urljoin

from src.core.entities.VirtualMachine import VirtualMachine
from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.FileSystemService import FileSystemService
from src.core.interfaces.services.VirtualMachinesInstallerService import VirtualMachinesInstallerService


class VirtualMachinesInstallerServiceImpl(VirtualMachinesInstallerService):
    def __init__(self,
                 storage_repository: StorageRepository,
                 virtual_machines_repository: VirtualMachinesRepository,
                 file_system_service: FileSystemService,
                 output_handler: OutputHandler,):
        self._storage_repository = storage_repository
        self._virtual_machines_repository = virtual_machines_repository
        self._file_system_service = file_system_service
        self._output_handler = output_handler

        self._ova_repo: Optional[str] = None
        self._ova_dir: Optional[str] = None

    def prepare(self) -> None:
        storage = self._storage_repository.get()
        self._ova_repo = storage.repository
        self._ova_dir = self._file_system_service.to_absolute_path(storage.ova_store_to)
        self._file_system_service.mkdirs(self._ova_dir)

    def install(self, no_verify_checksum: bool = False) -> None:
        self.prepare()

        for vm in self._virtual_machines_repository.get_all():
            ova_url = urljoin(self._ova_repo, vm.ova_filename)
            download_path = os.path.join(self._ova_dir, f"{vm.name}.ova")
            download_needed = self._is_download_needed(vm, download_path, no_verify_checksum)

            if download_needed:
                self._output_handler.new_progress_bar()
                self._file_system_service.download_file(ova_url, download_path, self._output_handler)



    def _is_download_needed(self,vm: VirtualMachine, download_path: str, no_verify_checksum: bool) -> bool:
        if not os.path.exists(download_path):
            return True
        else:
            if not no_verify_checksum:
                if vm.md5checksum != self._file_system_service.calc_md5(download_path):
                    return True

        return False