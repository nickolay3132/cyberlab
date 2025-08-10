import subprocess
from typing import List

from src.core.entities import VM, Snapshot
from src.core.interfaces.gateways import IVmsSnapshotsGateway


class VmsSnapshotsGateway(IVmsSnapshotsGateway):
    def create_snapshot(self, vm: VM, snapshot: Snapshot) -> bool:
        return self.run_process([
            "VBoxManage", "snapshot", vm.name,
            "take", f"{snapshot.timestamp}-{snapshot.name}",
            "--description", snapshot.description,
        ])

    def restore_snapshot(self, vm: VM, snapshot: Snapshot) -> bool:
        return self.run_process([
            "VBoxManage", "snapshot", vm.name,
            "restore", f"{snapshot.timestamp}-{snapshot.name}"
        ])

    @staticmethod
    def run_process(cmd: List[str]) -> bool:
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

        return process.returncode == 0