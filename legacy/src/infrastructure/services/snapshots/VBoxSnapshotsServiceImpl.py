import asyncio
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from typing import List

from src.core.entities.Snapshot import Snapshot
from src.core.entities.VirtualMachine import VirtualMachine
from src.core.entities.event_bus import EventBus
from src.core.entities.event_bus.events import StrEvent, SelectOptionEvent, SnapshotsTreeEvent, StrEventTypes
from src.core.interfaces.repositories.SnapshotsRepository import SnapshotsRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService

@dataclass
class VBoxSnapshotsServiceImpl(VBoxSnapshotsService):
    virtual_machines_repository: VirtualMachinesRepository
    snapshots_repository: SnapshotsRepository

    str_event_bus: EventBus[StrEvent]
    select_option_event_bus: EventBus[SelectOptionEvent]
    snapshots_tree_event_bus: EventBus[SnapshotsTreeEvent]

    timestamp = int(time.time())
    index_to_restore = 0

    def create_snapshot(self, vm: VirtualMachine, snapshot_name: str, description: str = '') -> None:
        cmd = [
            "VBoxManage", "snapshot", vm.name,
            "take", snapshot_name,
            "--description", description,
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

        self.str_event_bus.notify(StrEvent(vm.name, StrEventTypes.SUCCESS, 'Snaphsot created'))

    def create_snapshot_for_all(self, snapshot_name: str, description: str = '') -> None:
        timestamp = int(time.time())

        current_snapshot = self.snapshots_repository.get_current_snapshot()
        snapshot_name = snapshot_name.replace(' ', '-')
        needed_to_create = self.snapshots_repository.add_snapshot(Snapshot(
            name=snapshot_name,
            description=description,
            timestamp=timestamp,
            is_current=True,
            children=[],
        ), current_snapshot.name if current_snapshot is not None else None)

        if needed_to_create:

            for vm in self.virtual_machines_repository.get_all():
                self.str_event_bus.notify(StrEvent(vm.name, StrEventTypes.TEXT, 'Creating snapshot'))
                self.create_snapshot(vm, f"{timestamp}-{snapshot_name}", description)

    def list_snapshots(self) -> None:
        snapshots = self.snapshots_repository.get_root_snapshot()
        if not snapshots:
            self.str_event_bus.notify(StrEvent('main', StrEventTypes.ERROR, 'No snapshots found'))
            return
        self.snapshots_tree_event_bus.notify(SnapshotsTreeEvent('dialog', snapshots))

    def restore_snapshot(self, name: str) -> None:
        snapshots = self.snapshots_repository.find_all_snapshots(name)

        try:
            snapshot = self.get_snapshot_to_restore(snapshots)
        except IndexError:
            self.str_event_bus.notify(StrEvent('main', StrEventTypes.ERROR, 'Snapshot not found'))
            return

        need_to_restore = self.snapshots_repository.restore_snapshot(snapshot)
        if need_to_restore:
            for vm in self.virtual_machines_repository.get_all():
                cmd = ["VBoxManage", "snapshot", vm.name, "restore", f"{snapshot.timestamp}-{snapshot.name}"]
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                process.wait()

        self.str_event_bus.notify(StrEvent('main', StrEventTypes.SUCCESS, f'Snapshot restored to {snapshot.name}'))

    def get_snapshot_to_restore(self, snapshots: List[Snapshot]) -> Snapshot:
        index_to_restore = 0

        if len(snapshots) > 1:
            snapshots_data = [f"{datetime.fromtimestamp(s.timestamp)} {s.name}" for s in snapshots]
            index_to_restore = self.select_snapshot(snapshots_data)

        return snapshots[index_to_restore]

    def select_snapshot(self, snapshots_data: List[str]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def select_snapshot_async():
            future = asyncio.get_event_loop().create_future()

            event = SelectOptionEvent('dialog', snapshots_data, future)
            self.select_option_event_bus.notify(event)

            return await future

        return asyncio.get_event_loop().run_until_complete(select_snapshot_async())
