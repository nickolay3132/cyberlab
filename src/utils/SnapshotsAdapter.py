import subprocess
import sys
import time
from typing import List

from colorama.ansi import Fore


class SnapshotAdapter:
    @staticmethod
    def _run_base_process(cmd: List[str]) -> None:
        process = subprocess.Popen(cmd)
        process.wait()
        print()
        return None

    @staticmethod
    def create(vm_name: str, snapshot_name: str, description: str = "") -> None:
        return SnapshotAdapter._run_base_process([
            "VBoxManage", "snapshot", vm_name,
            "take", snapshot_name,
            "--description", description,
        ])

    @staticmethod
    def list(vm_name: str):
        cmd = [
            "VBoxManage", "snapshot", vm_name, "list"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            if "Could not find a registered machine named" in stderr:
                raise Exception(f"{Fore.RED}Could not find a virtual machine named {vm_name}")
            else:
                print(stderr)
                sys.exit(1)

        return stdout.strip()

    @staticmethod
    def restore(vm_name: str, snapshot_name: str) -> None:
        return SnapshotAdapter._run_base_process([
            "VBoxManage", "snapshot", vm_name, "restore", snapshot_name,
        ])

    @staticmethod
    def delete(vm_name: str, snapshot_name: str) -> None:
        return SnapshotAdapter._run_base_process([
            "VBoxManage", "snapshot", vm_name, "delete", snapshot_name,
        ])