from dataclasses import dataclass

from src.core.interfaces.services.VBoxManageService import VBoxManageService
from src.core.interfaces.services.VirtualMachinesInstallerService import VirtualMachinesInstallerService


@dataclass
class InstallCommandDTO:
    skip_download: bool = False
    no_verify: bool = False

class InstallCommand:
    def __init__(
            self,
            virtual_machines_installer_service: VirtualMachinesInstallerService,
            vboxmanage_service: VBoxManageService,
    ):
        self.virtual_machines_installer_service = virtual_machines_installer_service
        self.vboxmanage_service = vboxmanage_service

    def execute(self, dto: InstallCommandDTO):
        if not dto.skip_download:
            self.virtual_machines_installer_service.install()

        self.vboxmanage_service.import_vms()