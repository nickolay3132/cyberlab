from dataclasses import dataclass
from typing import Optional

from src.core.entities import Snapshot
from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import TextEvent
from src.core.enums.events import TextEventType
from src.core.interfaces.repositories import ISnapshotsRepository, IVMRepository
from src.core.interfaces.services.vms import IVmSnapshotsService


@dataclass
class RestoreSnapshotUseCaseDto:
    name: str
    timestamp: Optional[int] = None

@dataclass
class RestoreSnapshotUseCase:
    ev_bus: IEventBus

    snapshots_repo: ISnapshotsRepository
    vms_repo: IVMRepository

    snapshots_service: IVmSnapshotsService

    def execute(self, dto: RestoreSnapshotUseCaseDto):
        snapshot: Optional[Snapshot] = None

        if dto.timestamp is not None:
            snapshot = self.snapshots_repo.find_by_identity(dto.name, dto.timestamp)

        if snapshot is None or not self.snapshots_repo.restore_snapshot(snapshot):
            self.ev_bus.notify(TextEvent('main', TextEventType.ERROR, f'Cannot find snapshot with name "{dto.name}"'))
            return

        self.ev_bus.notify(TextEvent('main', TextEventType.TEXT, f'Restoring snapshot "{dto.name}"'))

        for vm in self.vms_repo.get_all():
            self.snapshots_service.restore_snapshot(vm, snapshot)

        self.ev_bus.notify(TextEvent('main', TextEventType.SUCCESS, 'Snapshot restored successfully'))

    # TODO: implement CLI support (without timestamp)
