import subprocess
import time
from dataclasses import dataclass
from datetime import datetime

from src.core.entities.Snapshot import Snapshot
from src.core.entities.VirtualMachine import VirtualMachine
from src.core.interfaces.input.InputHandler import InputHandler
from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.SnapshotsRepository import SnapshotsRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService
from src.core.interfaces.services.snapshots.SnapshotsTreeService import SnapshotsTreeService

@dataclass
class VBoxSnapshotsServiceImpl(VBoxSnapshotsService):
    virtual_machines_repository: VirtualMachinesRepository
    snapshots_repository: SnapshotsRepository
    output_handler: OutputHandler
    input_handler: InputHandler

    timestamp = int(time.time())
    index_to_restore = 0

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
        current_snapshot = self.snapshots_repository.get_current_snapshot()
        needed_to_create = self.snapshots_repository.add_snapshot(Snapshot(
            name=snapshot_name,
            description=description,
            timestamp=self.timestamp,
            is_current=True,
            children=[],
        ), current_snapshot.name if current_snapshot is not None else None)

        if needed_to_create:
            for vm in self.virtual_machines_repository.get_all():
                self.create_snapshot(vm, snapshot_name, description)

    def list_snapshots(self) -> None:
        snapshots = self.snapshots_repository.get_root_snapshot()

        self.output_handler.snapshots_tree(snapshots)

    def restore_snapshot(self, name: str) -> None:
        snapshots = self.snapshots_repository.find_all_snapshots(name)
        if len(snapshots) > 1:
            snapshots_data = [f"{datetime.fromtimestamp(s.timestamp)} {s.name}" for s in snapshots]
            self.input_handler.select_option(snapshots_data, self.select_snapshot_callback)

        snapshot = snapshots[self.index_to_restore]
        need_to_restore = self.snapshots_repository.restore_snapshot(snapshot)
        if need_to_restore:
            for vm in self.virtual_machines_repository.get_all():
                cmd = ["VBoxManage", "snapshot", vm.name, "restore", f"{snapshot.timestamp}-{snapshot.name}"]
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.wait()

        self.output_handler.success(f"Snapshot restored to {snapshot.name}")

    def select_snapshot_callback(self, index: int) -> None:
        self.index_to_restore = index
