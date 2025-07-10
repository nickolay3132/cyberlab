import subprocess
from dataclasses import dataclass
from typing import List

from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService

@dataclass
class VBoxBootServiceImpl(VBoxBootService):
    virtual_machines_repository: VirtualMachinesRepository
    output_handler: OutputHandler

    def startup(self) -> None:
        for vm in self.virtual_machines_repository.get_all():
            cmd = [
                "VBoxManage", "startvm", vm.name, "--type", vm.boot_policy.startup
            ]
            self.output_handler.text(f"Starting {vm.name}")
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

            self.output_handler.text(f"Stopping {vm.name}")
            self._run_process(cmd, vm.name, action='stop')

    def _run_process(self, cmd: List[str], vm_name: str, action: str) -> None:
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        process.wait()

        if process.returncode == 0:
            self.output_handler.success(f"{vm_name} {'started' if action == 'start' else 'stopped'} successfully")
        else:
            self.output_handler.show_error(f"could not {'start' if action == 'start' else 'stop'} {vm_name}. {process.stderr.read()}")

        self.output_handler.space()

