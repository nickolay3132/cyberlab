from dataclasses import dataclass

from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCase, CreateSnapshotUseCaseDTO
from src.core.use_cases.snapshots.ListSnapshotsUseCase import ListSnapshotsUseCase, ListSnapshotsUseCaseDTO


@dataclass
class SnapshotCommands:
    create_snapshot_use_case: CreateSnapshotUseCase
    list_snapshots_use_case: ListSnapshotsUseCase

    def create(self, args):
        self.create_snapshot_use_case.execute(CreateSnapshotUseCaseDTO(
            name=args.name,
            description=args.description,
        ))

    def list(self, args):
        self.list_snapshots_use_case.execute(ListSnapshotsUseCaseDTO())

    def restore(self, args):
        print("Restoring snapshot command")

    def delete(self, args):
        print("Deleting snapshot command")