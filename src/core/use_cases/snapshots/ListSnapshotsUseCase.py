from dataclasses import dataclass

from src.core.entities.observer import Subject
from src.core.interfaces.services.snapshots import VBoxSnapshotsService


@dataclass
class ListSnapshotsUseCaseDTO:
    pass

@dataclass
class ListSnapshotsUseCase:
    vbox_snapshots_service: VBoxSnapshotsService

    subject: Subject

    def execute(self, dto: ListSnapshotsUseCaseDTO) -> None:
        self.vbox_snapshots_service.list_snapshots(self.subject)