import os
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from src.core.entities.VirtualMachine import VirtualMachine
from src.core.entities.observer import Subject, ObserverEvent
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.FileSystemService import FileSystemService
from src.core.interfaces.services.VirtualMachinesInstallerService import VirtualMachinesInstallerService

@dataclass
class VirtualMachinesInstallerServiceImpl(VirtualMachinesInstallerService):
    storage_repository: StorageRepository
    virtual_machines_repository: VirtualMachinesRepository
    file_system_service: FileSystemService

    _ova_repo: Optional[str] = None
    _ova_dir: Optional[str] = None

    _subject: Optional[Subject] = None

    def set_subject(self, subject: Subject) -> 'VirtualMachinesInstallerService':
        self._subject = subject
        return self

    def prepare(self) -> None:
        storage = self.storage_repository.get()
        self._ova_repo = storage.repository
        self._ova_dir = self.file_system_service.to_absolute_path(storage.ova_store_to)
        self.file_system_service.mkdirs(self._ova_dir)

    def install(self, no_verify_checksum: bool = False) -> None:
        self.prepare()

        self._subject.notify(ObserverEvent.title(
            id='main',
            data="Downloading OVA files"
        ))

        for vm in self.virtual_machines_repository.get_all():
            ova_url = urljoin(self._ova_repo, vm.ova_filename)
            download_path = os.path.join(self._ova_dir, f"{vm.name}.ova")
            download_needed = self._is_download_needed(vm, download_path, no_verify_checksum)

            if download_needed:
                # self._subject.notify(ObserverEvent.text(id=vm.name, data = f"Downloading {vm.name}",))
                self.file_system_service.download_file(
                    url=ova_url,
                    download_path=download_path,
                    download_id=vm.name,
                    subject=self._subject
                )
            else:
                self._subject.notify(ObserverEvent.warning(id=vm.name, data=f"{vm.name} already exists. Skipping..."))



    def _is_download_needed(self,vm: VirtualMachine, download_path: str, no_verify_checksum: bool) -> bool:
        if not os.path.exists(download_path):
            return True
        else:
            if not no_verify_checksum:
                if vm.md5checksum != self.file_system_service.calc_md5(download_path):
                    return True

        return False