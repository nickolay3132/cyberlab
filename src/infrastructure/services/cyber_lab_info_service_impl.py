import subprocess

from src.core.entities.VirtualMachine import VirtualMachine
from src.core.interfaces.services.cyber_lab_info_service import CyberLabInfoService


class CyberLabInfoServiceImpl(CyberLabInfoService):
    def is_installed(self, vm: VirtualMachine) -> bool:
        result = subprocess.run(
            ["VBoxManage", "list", "vms"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.splitlines():
            if f'"{vm.name}"' in line:
                return True

        return False

    def is_running(self, vm: VirtualMachine) -> bool:
        result = subprocess.run(
            ["VBoxManage", "showvminfo", vm.name, "--machinereadable"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.splitlines():
            if line.startswith("VMState="):
                vm_state = line.split('=')[1].strip('"')
                is_running = vm_state == "running"
                return vm_state == "running"

        return False