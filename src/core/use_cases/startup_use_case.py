from dataclasses import dataclass

from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import TextEvent
from src.core.enums.events import TextEventType
from src.core.interfaces.repositories import IVMRepository
from src.core.interfaces.services.vms import IVmBootService


@dataclass
class StartupUseCaseDto: pass

@dataclass
class StartupUseCase:
    vms_repo: IVMRepository

    vm_boot_service: IVmBootService

    ev_bus: IEventBus

    def execute(self, dto: StartupUseCaseDto) -> None:
        for vm in self.vms_repo.get_all():
            self.ev_bus.notify(TextEvent(vm.name, TextEventType.TEXT, "starting..."))
            is_success = self.vm_boot_service.startup(vm.name, vm.boot_policy.startup)

            if is_success:
                self.ev_bus.notify(TextEvent(vm.name, TextEventType.SUCCESS, "vm is running"))
            else:
                self.ev_bus.notify(TextEvent(vm.name, TextEventType.WARNING, "unable to start VM (it may already be running)"))