import subprocess
import threading
import os
import time

from typing import Literal


class VboxManagerAdapter:
    @staticmethod
    def create_nat_network() -> bool:
        nat_networks = subprocess.run(
            ["VBoxManage", "list", "natnetworks"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if not 'cyberlab' in nat_networks.stdout.lower():
            cmd = [
                "VBoxManage", "natnetwork", "add",
                "--netname", "cyberlab",
                "--network", "10.0.2.0/24",
                "--enable",
                "--dhcp", "on"
            ]

            process = subprocess.Popen(cmd)
            process.wait()
            print()
            return process.returncode == 0
        else:
            return True

    @staticmethod
    def enable_nat_network(vm_name: str, nic_index: int, nat_name: str) -> bool:
        cmd = [
            "VBoxManage", "modifyvm", vm_name,
            f"--nic{nic_index}", "natnetwork",
            f"--nat-network{nic_index}", nat_name,
            f"--cableconnected{nic_index}", "on"
        ]
        process = subprocess.Popen(cmd)
        process.wait()
        print()
        return process.returncode == 0

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

