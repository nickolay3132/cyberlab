import subprocess
import time
from dataclasses import dataclass

from src.core.entities.VirtualMachine import VirtualMachine
from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotService

@dataclass
class VBoxSnapshotServiceImpl(VBoxSnapshotService):
    virtual_machines_repository: VirtualMachinesRepository

    output_handler: OutputHandler

    timestamp = int(time.time())

    def create_snapshot(self, vm: VirtualMachine, snapshot_name: str, description: str = '') -> None:
        cmd = [
            "VBoxManage", "snapshot", vm.name,
            "take", f"{self.timestamp}-{snapshot_name}",
            "--description", description,
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

        self.output_handler.success(f"Snapshot for {vm.name} created")

    def create_snapshot_for_all(self, snapshot_name: str, description: str = '') -> None:
        for vm in self.virtual_machines_repository.get_all():
            self.create_snapshot(vm, snapshot_name, description)