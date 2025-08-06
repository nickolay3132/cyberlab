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

    text_ev_bus: IEventBus[TextEvent]

    def execute(self, dto: ShutdownUseCaseDto) -> None:
        for vm in self.vms_repo.get_all():
            self.text_ev_bus.notify(TextEvent(vm.name, TextEventType.TEXT, "stopping..."))
            is_success = self.vm_boot_service.shutdown(vm.name, vm.boot_policy.shutdown, force=dto.force)

            if is_success:
                self.text_ev_bus.notify(TextEvent(vm.name, TextEventType.SUCCESS, "stopped successfully"))
            else:
                self.text_ev_bus.notify(TextEvent(vm.name, TextEventType.WARNING, "cannot stop vm"))
