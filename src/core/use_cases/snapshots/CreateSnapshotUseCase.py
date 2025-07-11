from dataclasses import dataclass

from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService


@dataclass
class CreateSnapshotUseCaseDTO:
    name: str
    description: str = ""

@dataclass
class CreateSnapshotUseCase:
    vbox_snapshots_service: VBoxSnapshotsService

    def execute(self, dto: CreateSnapshotUseCaseDTO):
        self.vbox_snapshots_service.create_snapshot_for_all(dto.name, dto.description)
