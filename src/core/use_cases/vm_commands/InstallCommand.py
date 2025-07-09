from dataclasses import dataclass

from src.core.interfaces.output.OutputHandler import OutputHandler
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
            output_handler: OutputHandler,
    ):
        self.virtual_machines_installer_service = virtual_machines_installer_service
        self.vboxmanage_service = vboxmanage_service
        self.output_handler = output_handler

    def execute(self, dto: InstallCommandDTO):
        if not dto.skip_download:
            self.virtual_machines_installer_service.install(no_verify_checksum=dto.no_verify)

        if not self.vboxmanage_service.networks().create_nat_net():
            self.output_handler.show_error("Could not create NAT network", terminate=True)

        self.vboxmanage_service.import_vms()
        self.vboxmanage_service.enable_networks()