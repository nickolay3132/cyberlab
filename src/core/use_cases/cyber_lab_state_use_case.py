from dataclasses import dataclass

from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.core.enums.events import TextEventType
from src.core.interfaces.gateways import IVMsGateway
from src.core.interfaces.repositories import IVMRepository, IStorageRepository
from src.core.interfaces.services import IFileSystemService


@dataclass
class CyberLabStateUseCaseDto:
    pass

@dataclass
class CyberLabStateUseCase:
    vm_gateway: IVMsGateway
    ev_bus: IEventBus
    vms_repo: IVMRepository
    storage_repo: IStorageRepository
    filesystem_service: IFileSystemService

    def execute(self, dto: CyberLabStateUseCaseDto):
        ova_dir = self.storage_repo.get().ova_store_to
        vms = self.vms_repo.get_all()
        self.ev_bus.notify(VmsListEvent([vm.name for vm in vms]))

        for vm in vms:
            vm_ova_filepath = f"{ova_dir}/{vm.name}.ova"
            if not self.filesystem_service.file_exists(vm_ova_filepath):
                state = "not installed"
            else:
                if self.vm_gateway.is_running(vm):
                    state = "vm is running"
                else:
                    state = "vm is not stopped"

            self.ev_bus.notify(TextEvent(vm.name, TextEventType.TEXT, state))
