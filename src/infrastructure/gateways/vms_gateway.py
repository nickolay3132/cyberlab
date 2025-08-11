import subprocess

from src.core.entities import VM
from src.core.interfaces.gateways import IVMsGateway


class VmsGatewayImpl(IVMsGateway):
    def import_vm(self, ova_path: str, vm_name: str, vms_dir: str, log_file) -> int:
        cmd = [
            "VBoxManage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", vms_dir,
        ]

        process = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=log_file,
            text=True,
            encoding="utf-8"
        )
        process.wait()
        return process.returncode

    def is_running(self, vm: VM) -> bool:
        try:
            result = subprocess.run(
                ["VBoxManage", "showvminfo", vm.name, "--machinereadable"],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            if result.returncode != 0:
                return False

            for line in result.stdout.splitlines():
                if line.startswith("VMState="):
                    state = line.split("=")[1].strip().strip('"')
                    return state == "running"
            return False
        except Exception:
            return False