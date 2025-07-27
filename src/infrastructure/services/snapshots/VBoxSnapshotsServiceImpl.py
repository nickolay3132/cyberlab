import asyncio
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.core.entities.Snapshot import Snapshot
from src.core.entities.VirtualMachine import VirtualMachine
from src.core.entities.observer import Subject, ObserverEvent
from src.core.interfaces.repositories.SnapshotsRepository import SnapshotsRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService

@dataclass
class VBoxSnapshotsServiceImpl(VBoxSnapshotsService):
    virtual_machines_repository: VirtualMachinesRepository
    snapshots_repository: SnapshotsRepository

    timestamp = int(time.time())
    index_to_restore = 0

    def create_snapshot(self, subject: Subject, vm: VirtualMachine, snapshot_name: str, description: str = '') -> None:
        cmd = [
            "VBoxManage", "snapshot", vm.name,
            "take", f"{self.timestamp}-{snapshot_name.replace(' ', '')}",
            "--description", description,
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

        subject.notify(ObserverEvent.success(vm.name, 'Snapshot created'))

    def create_snapshot_for_all(self, subject: Subject, snapshot_name: str, description: str = '') -> None:
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
                self.create_snapshot(subject, vm, snapshot_name, description)

    def list_snapshots(self, subject: Subject) -> None:
        snapshots = self.snapshots_repository.get_root_snapshot()
        subject.notify(ObserverEvent.display_snapshot_tree(snapshots))

    def restore_snapshot(self, name: str, subject: Subject) -> None:
        snapshots = self.snapshots_repository.find_all_snapshots(name)

        snapshot = self.get_snapshot_to_restore(snapshots, subject)
        need_to_restore = self.snapshots_repository.restore_snapshot(snapshot)
        if need_to_restore:
            for vm in self.virtual_machines_repository.get_all():
                cmd = ["VBoxManage", "snapshot", vm.name, "restore", f"{snapshot.timestamp}-{snapshot.name}"]
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.wait()

        subject.notify(ObserverEvent.success('main', f"Snapshot restored to {snapshot.name}"))

    def get_snapshot_to_restore(self, snapshots: List[Snapshot], subject: Subject) -> Snapshot:
        index_to_restore = 0

        if len(snapshots) > 1:
            snapshots_data = [f"{datetime.fromtimestamp(s.timestamp)} {s.name}" for s in snapshots]
            index_to_restore = self.select_snapshot(subject, snapshots_data)

        return snapshots[index_to_restore]

    @staticmethod
    def select_snapshot(subject: Subject, snapshot_data: List[str]):
        async def select_snapshot_async():
            future = asyncio.get_event_loop().create_future()

            event = ObserverEvent.select_option('dialog', snapshot_data, future)
            subject.notify(event)

            return await future

        return asyncio.get_event_loop().run_until_complete(select_snapshot_async())
