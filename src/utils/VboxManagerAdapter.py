import subprocess
import threading
import os
import time

from typing import Literal


class VboxManagerAdapter:
    @staticmethod
    def import_vm(ova_path: str, vm_name: str, vms_dir: str, log_file: str) -> bool:
        cmd = [
            "VBoxManage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", vms_dir
        ]

        try:
            with open(log_file, "w") as log:
                log.write(f"Starting import of {vm_name} from {ova_path}\n")

                process = subprocess.Popen(
                    cmd,
                    stdout=log,
                    stderr=log,
                    text=True,
                    encoding="utf-8"
                )

                process.wait()
                return process.returncode == 0

        except Exception as e:
            with open(log_file, "a") as log:
                log.write(f"Exception during import: {str(e)}\n")
            return False


    @staticmethod
    def start_vm(vm_name: str, launch_type: Literal["gui", "headless", "separate"] = "gui") -> bool:
        cmd = [
            "VBoxManage", "startvm", vm_name, "--type", launch_type,
        ]

        process = subprocess.Popen(cmd)
        process.wait()
        print()
        return process.returncode == 0

    @staticmethod
    def stop_vm(vm_name: str, shutdown_type: Literal["acpipowerbutton", "poweroff", "savestate"]) -> bool:
        cmd = [
            "VBoxManage", "controlvm", vm_name, shutdown_type
        ]

        process = subprocess.Popen(cmd)
        process.wait()
        print()
        return process.returncode == 0

