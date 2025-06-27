import subprocess
from typing import Literal


class VboxManagerAdapter:
    @staticmethod
    def import_vm(ova_path: str, vm_name: str, vms_dir: str) -> bool:
        print(f"\nImporting {vm_name}...")
        cmd = [
            "VBoxManage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", vms_dir
        ]

        process = subprocess.Popen(cmd)
        process.wait()

        return process.returncode == 0

    @staticmethod
    def start_vm(vm_name: str, launch_type: Literal["gui", "headless", "separate"] = "gui") -> bool:
        cmd = [
            "VBoxManage", "startvm", vm_name, "--type", launch_type,
        ]

        process = subprocess.Popen(cmd)
        process.wait()
        return process.returncode == 0

    @staticmethod
    def stop_vm(vm_name: str, shutdown_type: Literal["acpipowerbutton", "poweroff", "savestate"]) -> bool:
        print(f"\nStopping {vm_name}...")
        cmd = [
            "VBoxManage", "controlvm", vm_name, shutdown_type
        ]

        process = subprocess.Popen(cmd)
        process.wait()

        return process.returncode == 0

