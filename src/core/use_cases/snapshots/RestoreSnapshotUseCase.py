from dataclasses import dataclass

from src.core.entities.observer import Subject
from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService


@dataclass
class RestoreSnapshotUseCaseDTO:
    name: str

@dataclass
class RestoreSnapshotUseCase:
    vbox_snapshots_service: VBoxSnapshotsService

    subject = Subject()

    def execute(self, dto: RestoreSnapshotUseCaseDTO) -> None:
        self.vbox_snapshots_service.restore_snapshot(dto.name, self.subject)