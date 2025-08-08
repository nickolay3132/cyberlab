from dataclasses import dataclass

from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import TextEvent
from src.core.enums.events import TextEventType
from src.core.interfaces.repositories import IVMRepository
from src.core.interfaces.services.vms import IVmBootService


@dataclass
class ShutdownUseCaseDto:
    force: bool

@dataclass
class ShutdownUseCase:
    vms_repo: IVMRepository

    vm_boot_service: IVmBootService

    ev_bus: IEventBus

    def execute(self, dto: ShutdownUseCaseDto) -> None:
        for vm in self.vms_repo.get_all():
            self.ev_bus.notify(TextEvent(vm.name, TextEventType.TEXT, "stopping..."))
            is_success = self.vm_boot_service.shutdown(vm.name, vm.boot_policy.shutdown, force=dto.force)

            if is_success:
                self.ev_bus.notify(TextEvent(vm.name, TextEventType.SUCCESS, "vm is stopped"))
            else:
                self.ev_bus.notify(TextEvent(vm.name, TextEventType.WARNING, "unable to stop VM (it may already be stopped)"))
