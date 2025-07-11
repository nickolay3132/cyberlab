from dataclasses import dataclass

from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotService


@dataclass
class CreateSnapshotUseCaseDTO:
    name: str
    description: str = ""

@dataclass
class CreateSnapshotUseCase:
    vbox_snapshot_service: VBoxSnapshotService

    def execute(self, dto: CreateSnapshotUseCaseDTO):
        self.vbox_snapshot_service.create_snapshot_for_all(dto.name, dto.description)
