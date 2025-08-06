import subprocess

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