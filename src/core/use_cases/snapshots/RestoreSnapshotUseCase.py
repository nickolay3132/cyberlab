from dataclasses import dataclass

from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService


@dataclass
class RestoreSnapshotUseCaseDTO:
    name: str

@dataclass
class RestoreSnapshotUseCase:
    vbox_snapshots_service: VBoxSnapshotsService

    def execute(self, dto: RestoreSnapshotUseCaseDTO) -> None:
        self.vbox_snapshots_service.restore_snapshot(dto.name)