import subprocess
from dataclasses import dataclass
from typing import List

from src.core.entities.event_bus import EventBus
from src.core.entities.event_bus.events import StrEvent, StrEventTypes
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService

@dataclass
class VBoxBootServiceImpl(VBoxBootService):
    virtual_machines_repository: VirtualMachinesRepository

    str_event_bus: EventBus[StrEvent]

    def startup(self) -> None:
        for vm in self.virtual_machines_repository.get_all():
            cmd = [
                "VBoxManage", "startvm", vm.name, "--type", vm.boot_policy.startup
            ]
            self.str_event_bus.notify(StrEvent(vm.name, StrEventTypes.TEXT, 'Starting...'))
            self._run_process(cmd, vm.name, action='start')

    def shutdown(self, force: bool = False) -> None:
        for vm in self.virtual_machines_repository.get_all():
            cmd = [
                "VBoxManage", "controlvm", vm.name
            ]

            if force:
                cmd.append("poweroff")
            else:
                cmd.append(vm.boot_policy.shutdown)

            self.str_event_bus.notify(StrEvent(vm.name, StrEventTypes.TEXT, 'Stopping...'))
            self._run_process(cmd, vm.name, action='stop')

    def _run_process(self, cmd: List[str], vm_name: str, action: str) -> None:
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        process.wait()

        if process.returncode == 0:
            self.str_event_bus.notify(StrEvent(
                vm_name,
                StrEventTypes.SUCCESS,
                f"{'Started' if action == 'start' else 'Stopped'} successfully"
            ))
        else:
            self.str_event_bus.notify(StrEvent(
                vm_name,
                StrEventTypes.ERROR,
                f"Could not {'start' if action == 'start' else 'stop'}."
            ))
        self.str_event_bus.notify(StrEvent('main', StrEventTypes.SPACE, ''))

