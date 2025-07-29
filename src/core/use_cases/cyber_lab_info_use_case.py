from dataclasses import dataclass

from src.core.entities.event_bus import EventBus
from src.core.entities.event_bus.events import StrEvent, StrEventTypes
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.cyber_lab_info_service import CyberLabInfoService


@dataclass
class CyberLabInfoUseCase:
    vms_repository: VirtualMachinesRepository
    cyber_lab_info_service: CyberLabInfoService
    info_event_bus: EventBus[StrEvent]

    no_display: bool

    def execute(self):
        if self.no_display:
            return

        for vm in self.vms_repository.get_all():
            if not self.cyber_lab_info_service.is_installed(vm):
                self.info_event_bus.notify(StrEvent(vm.name, StrEventTypes.TEXT, 'vm is not installed'))
            else:
                if not self.cyber_lab_info_service.is_running(vm):
                    self.info_event_bus.notify(StrEvent(vm.name, StrEventTypes.TEXT, 'vm is stopped'))
                else:
                    self.info_event_bus.notify(StrEvent(vm.name, StrEventTypes.TEXT, 'vm is running'))

        self.info_event_bus.notify(StrEvent('main', StrEventTypes.TEXT, ''))

