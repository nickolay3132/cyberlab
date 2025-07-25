from dataclasses import dataclass

from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCase, CreateSnapshotUseCaseDTO
from src.core.use_cases.snapshots.ListSnapshotsUseCase import ListSnapshotsUseCase, ListSnapshotsUseCaseDTO
from src.core.use_cases.snapshots.RestoreSnapshotUseCase import RestoreSnapshotUseCase, RestoreSnapshotUseCaseDTO
from src.presentation.cli.commands.BaseCommands import InstallObserver


@dataclass
class SnapshotCommands:
    create_snapshot_use_case: CreateSnapshotUseCase
    list_snapshots_use_case: ListSnapshotsUseCase
    restore_snapshot_use_case: RestoreSnapshotUseCase

    def create(self, args):
        self.create_snapshot_use_case.subject.attach(InstallObserver())
        self.create_snapshot_use_case.execute(CreateSnapshotUseCaseDTO(
            name=args.name,
            description=args.description,
        ))

    def list(self, args):
        self.list_snapshots_use_case.subject.attach(InstallObserver())
        self.list_snapshots_use_case.execute(ListSnapshotsUseCaseDTO())

    def restore(self, args):
        self.restore_snapshot_use_case.subject.attach(InstallObserver())
        self.restore_snapshot_use_case.execute(RestoreSnapshotUseCaseDTO(
            name=args.name,
        ))

    def delete(self, args):
        print("Deleting snapshot command")