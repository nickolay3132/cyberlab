from dataclasses import dataclass, field
from typing import Any, List

from src.core.entities.observer import Subject, Observer, ObserverEvent
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

    subject: Subject = Subject()

    def execute(self, dto: InstallUseCaseDTO):
        if not dto.skip_download:
            self.virtual_machines_installer_service.set_subject(self.subject)
            self.virtual_machines_installer_service.install(no_verify_checksum=dto.no_verify)

        if not self.vboxmanage_service.networks().create_nat_net():
            self.subject.notify(ObserverEvent.error(id="main", data="Could not create NAT network"))

        self.vboxmanage_service.import_vms(self.subject)

        if False in self.vboxmanage_service.networks().enable_networks():
            self.subject.notify(ObserverEvent.error(id="main", data="Not all network adapters could be configured"))

        # self.vbox_snapshots_service.create_snapshot_for_all("initial-snapshot")