from dataclasses import dataclass

from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.FileSystemService import FileSystemService
from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService
from src.core.interfaces.services.vbox.VBoxImportService import VBoxImportService, ImportVMsDTO
from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService
from src.core.interfaces.services.vbox.VBoxNetworksService import VBoxNetworksService

@dataclass
class VBoxManageServiceImpl (VBoxManageService):
    storage_repository: StorageRepository
    virtual_machines_repository: VirtualMachinesRepository
    file_system_service: FileSystemService
    vbox_networks_service: VBoxNetworksService
    vbox_import_service: VBoxImportService
    vbox_boot_service: VBoxBootService
    output_handler: OutputHandler

    def import_vms(self) -> None:
        storage = self.storage_repository.get()
        log_dir = self.file_system_service.to_absolute_path(storage.import_log_store_to)
        vms_dir = self.file_system_service.to_absolute_path(storage.vms_store_to)
        ova_path = self.file_system_service.to_absolute_path(storage.ova_store_to)

        self.file_system_service.mkdirs(log_dir, vms_dir)

        self.output_handler.space()
        self.output_handler.show("Importing VMS")

        self.vbox_import_service.import_vms(ImportVMsDTO(
            vms=self.virtual_machines_repository.get_all(),
            vms_dir=vms_dir,
            log_dir=log_dir,
            ova_dir=ova_path,
        ))

        return None

    def enable_networks(self) -> None:
        for vm in self.virtual_machines_repository.get_all():
            for nic in vm.nics:
                if nic.type == "natnetwork":
                    self.vbox_networks_service.enable_nat_network(vm, nic)

    def networks(self) -> VBoxNetworksService:
        return self.vbox_networks_service

    def boot(self) -> VBoxBootService:
        return self.vbox_boot_service

