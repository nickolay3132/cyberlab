from dataclasses import dataclass

from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService
from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService
from src.core.interfaces.services.VirtualMachinesInstallerService import VirtualMachinesInstallerService


@dataclass
class InstallUseCaseDTO:
    skip_download: bool = False
    no_verify: bool = False

@dataclass
class InstallUseCase:
    virtual_machines_installer_service: VirtualMachinesInstallerService
    vboxmanage_service: VBoxManageService
    vbox_snapshots_service: VBoxSnapshotsService
    output_handler: OutputHandler

    def execute(self, dto: InstallUseCaseDTO):
        if not dto.skip_download:
            self.virtual_machines_installer_service.install(no_verify_checksum=dto.no_verify)

        if not self.vboxmanage_service.networks().create_nat_net():
            self.output_handler.show_error("Could not create NAT network", terminate=True)

        self.vboxmanage_service.import_vms()

        if False in self.vboxmanage_service.networks().enable_networks():
            self.output_handler.show_error("Not all network adapters could be configured")

        self.vbox_snapshots_service.create_snapshot_for_all("initial-snapshot")