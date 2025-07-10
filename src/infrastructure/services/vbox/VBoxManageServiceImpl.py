from dataclasses import dataclass

from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService
from src.core.interfaces.services.vbox.VBoxImportService import VBoxImportService
from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService
from src.core.interfaces.services.vbox.VBoxNetworksService import VBoxNetworksService

@dataclass
class VBoxManageServiceImpl (VBoxManageService):
    vbox_networks_service: VBoxNetworksService
    vbox_import_service: VBoxImportService
    vbox_boot_service: VBoxBootService

    def import_vms(self) -> None:
        self.vbox_import_service.import_vms()

    def networks(self) -> VBoxNetworksService:
        return self.vbox_networks_service

    def boot(self) -> VBoxBootService:
        return self.vbox_boot_service

