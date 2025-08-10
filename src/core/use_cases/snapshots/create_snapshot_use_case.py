from dataclasses import dataclass
import time

from src.core.entities.event_bus.events import TextEvent
from src.core.entities import Snapshot
from src.core.entities.event_bus import IEventBus
from src.core.enums.events import TextEventType
from src.core.interfaces.repositories import ISnapshotsRepository, IVMRepository
from src.core.interfaces.services.vms import IVmSnapshotsService


@dataclass
class CreateSnapshotUseCaseDto:
    snapshot_name: str
    description: str = ''

@dataclass
class CreateSnapshotUseCase:
    ev_bus: IEventBus

    snapshots_repo: ISnapshotsRepository
    vms_repo: IVMRepository

    snapshots_service: IVmSnapshotsService

    def execute(self, dto: CreateSnapshotUseCaseDto) -> None:
        current_snapshot = self.snapshots_repo.get_current_snapshot()
        timestamp = int(time.time())
        snapshot_name = dto.snapshot_name.replace(' ', '-')
        new_snapshot = Snapshot(
            name=snapshot_name,
            description=dto.description,
            timestamp=timestamp,
            is_current=True,
            children=[]
        )

        needed_to_create = self.snapshots_repo.add_snapshot(new_snapshot, current_snapshot)
        if needed_to_create:
            self.ev_bus.notify(TextEvent('main', TextEventType.TITLE, f'Creating snapshot {snapshot_name} for each vm'))

            for vm in self.vms_repo.get_all():
                self.snapshots_service.create_snapshot(vm, new_snapshot)

            self.ev_bus.notify(TextEvent('main', TextEventType.SUCCESS, f'Snapshot {snapshot_name} created successfully'))

        else:
            self.ev_bus.notify(TextEvent('main', TextEventType.WARNING, f'Snapshot {snapshot_name} already exists'))
