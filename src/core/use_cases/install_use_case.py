from dataclasses import dataclass
import time
from typing import Optional, List
from urllib.parse import urljoin

from src.core.entities import Storage, VM, Snapshot
from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import VmsListEvent
from src.core.entities.event_bus.events.progress_event import ProgressEvent
from src.core.entities.event_bus.events.text_event import TextEvent
from src.core.enums import DownloadingType
from src.core.enums.events import TextEventType
from src.core.interfaces.repositories import IStorageRepository, IVMRepository, ISnapshotsRepository
from src.core.interfaces.services.vms import IInstallVMService, IVmNetworkService, IVmSnapshotsService
from src.core.interfaces.services.vms import IImportVMService


@dataclass
class InstallUseCaseDto:
    repository: str
    no_verify: bool
    skip_download: bool
    
@dataclass
class InstallUseCase:
    ev_bus: IEventBus

    storage_repo: IStorageRepository
    vm_repo: IVMRepository
    snapshots_repo: ISnapshotsRepository

    install_vm_service: IInstallVMService
    import_vm_service: IImportVMService
    vm_network_service: IVmNetworkService
    snapshots_service: IVmSnapshotsService

    importing_needed: bool = True
    downloading_now: str = ''
    log_dir: str = ''
    ova_dir: str = ''
    
    def execute(self, dto: InstallUseCaseDto):
        storage = self.storage_repo.get()
        vms = self.vm_repo.get_all()

        self.ev_bus.notify(VmsListEvent(['main', *[vm.name for vm in vms]]))

        if not dto.skip_download:
            self._install_ova_files(dto.no_verify, dto.repository, storage, vms)

        if self.importing_needed:
            self._import_vms(storage, vms)
            self._enable_networks(vms)

            initial_snapshot = Snapshot(
                name="initial-snapshot",
                description="Initial state after OVA import.",
                timestamp=int(time.time()),
                is_current=True,
                children=[]
            )
            self.snapshots_repo.add_snapshot(initial_snapshot, None)

            for vm in vms:
                self.snapshots_service.create_snapshot(vm, initial_snapshot)


    def _install_ova_files(self, no_verify: bool, repository: str, storage: Storage, vms: List[VM]):
        ova_dir = self.install_vm_service.prepare_storage(storage.ova_store_to)

        self.install_vm_service.set_no_verify_checksum(no_verify)
        self.install_vm_service.set_callback(self._installation_callback)

        self.ev_bus.notify(TextEvent('main', TextEventType.TITLE, "Downloading OVA files"))

        for vm in vms:
            ova_url = urljoin(repository, f"{vm.ova_filename}")
            download_path = f"{ova_dir}/{vm.name}.ova"
            self.downloading_now = vm.name

            is_downloading = self.install_vm_service.install(ova_url, download_path, vm.md5checksum)

            if not is_downloading:
                self.ev_bus.notify(TextEvent(
                    vm.name,
                    TextEventType.WARNING,
                    "OVA file already exists. Skipping..."
                ))

    def _import_vms(self, storage: Storage, vms: List[VM]):
        ova_dir, vms_dir, log_dir = self.import_vm_service.prepare_storage(
            storage.ova_store_to,
            storage.vms_store_to,
            storage.import_log_store_to
        )
        self.log_dir = log_dir

        self.import_vm_service.set_callback(self._importing_callback)

        self.ev_bus.notify(TextEvent('', TextEventType.SPACE, ""))
        self.ev_bus.notify(TextEvent('main', TextEventType.TITLE, "Importing OVA files"))

        for vm in vms:
            self.ev_bus.notify(TextEvent(vm.name, TextEventType.TEXT, "Importing VM"))
            self.import_vm_service.import_vm(vm, ova_dir, vms_dir, log_dir)

        self.ev_bus.notify(TextEvent('', TextEventType.SPACE, ""))
        self.import_vm_service.run()

    def _enable_networks(self, vms: List[VM]):
        for vm in vms:
            is_success = self.vm_network_service.enable_vm_nics(vm)
            if not is_success:
                self.ev_bus.notify(TextEvent(vm.name, TextEventType.WARNING, "Failed to enable networks"))

    def _installation_callback(self,
                               state: DownloadingType,
                               total: int,
                               actual: int,
                               error_msg: Optional[str]
                               ) -> None:
        event = ProgressEvent(self.downloading_now, state, total, actual, error_msg)

        if state == DownloadingType.FAILED:
            self.importing_needed = False

        self.ev_bus.notify(event)

    def _importing_callback(self, vm_name: str, success: bool) -> None:
        if success:
            self.ev_bus.notify(TextEvent(vm_name, TextEventType.SUCCESS, "Successfully imported"))
        else:
            self.ev_bus.notify(TextEvent('dialog', TextEventType.ERROR, f"{vm_name.capitalize()} import failed\nLog files at {self.log_dir}"))
            self.ev_bus.notify(TextEvent(vm_name, TextEventType.ERROR, "unable to import vm"))
            self.ev_bus.notify(TextEvent('', TextEventType.SPACE, ''))

