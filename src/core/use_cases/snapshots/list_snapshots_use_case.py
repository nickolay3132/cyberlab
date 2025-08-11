from dataclasses import dataclass
from pprint import pprint

from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import SnapshotsTreeEvent
from src.core.interfaces.repositories import ISnapshotsRepository


@dataclass
class ListSnapshotsUseCaseDto:
    pass

@dataclass
class ListSnapshotsUseCase:
    ev_bus: IEventBus

    snapshots_repo: ISnapshotsRepository

    def execute(self, dto: ListSnapshotsUseCaseDto):
        self.ev_bus.notify(SnapshotsTreeEvent(
            self.snapshots_repo.get_root_snapshot()
        ))