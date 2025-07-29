import time
from dataclasses import dataclass

from src.core.interfaces.services.snapshots.VBoxSnapshotsService import VBoxSnapshotsService
from src.core.use_cases.cyber_lab_info_use_case import CyberLabInfoUseCase


@dataclass
class CreateSnapshotUseCaseDTO:
    name: str
    description: str = ""

@dataclass
class CreateSnapshotUseCase:
    vbox_snapshots_service: VBoxSnapshotsService

    info_use_case: CyberLabInfoUseCase

    def execute(self, dto: CreateSnapshotUseCaseDTO):
        self.vbox_snapshots_service.create_snapshot_for_all(dto.name, dto.description)

        time.sleep(3)
        self.info_use_case.execute()
