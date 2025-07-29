import time
from dataclasses import dataclass

from src.core.entities.event_bus import EventBus
from src.core.entities.event_bus.events import StrEvent, StrEventTypes
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService
from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService
from src.core.interfaces.services.VirtualMachinesInstallerService import VirtualMachinesInstallerService
from src.core.use_cases.cyber_lab_info_use_case import CyberLabInfoUseCase


@dataclass
class InstallUseCaseDTO:
    skip_download: bool = False
    no_verify: bool = False

@dataclass
class InstallUseCase:
    virtual_machines_installer_service: VirtualMachinesInstallerService
    vboxmanage_service: VBoxManageService
    vbox_snapshots_service: VBoxSnapshotsService

    str_event_bus: EventBus[StrEvent]

    info_use_case: CyberLabInfoUseCase

    def execute(self, dto: InstallUseCaseDTO):
        if not dto.skip_download:
            self.virtual_machines_installer_service.install(no_verify_checksum=dto.no_verify)

        if not self.vboxmanage_service.networks().create_nat_net():
            self.str_event_bus.notify(StrEvent('main', StrEventTypes.ERROR, 'Could not create NAT network'))

        self.vboxmanage_service.import_vms()

        if False in self.vboxmanage_service.networks().enable_networks():
            self.str_event_bus.notify(StrEvent('main', StrEventTypes.ERROR, 'Not all network adapters could bo configured'))
        self.vbox_snapshots_service.create_snapshot_for_all("initial-snapshot")

        time.sleep(3)
        self.info_use_case.execute()