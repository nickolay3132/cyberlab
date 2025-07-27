from dataclasses import dataclass

from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCase, CreateSnapshotUseCaseDTO
from src.core.use_cases.snapshots.ListSnapshotsUseCase import ListSnapshotsUseCase, ListSnapshotsUseCaseDTO
from src.core.use_cases.snapshots.RestoreSnapshotUseCase import RestoreSnapshotUseCase, RestoreSnapshotUseCaseDTO
from src.presentation.cli.observers.select_option_cli_observer import SelectOptionCLIObserver
from src.presentation.cli.observers.snapshots_tree_cli_observer import SnapshotTreeCLIObserver
from src.presentation.cli.observers.texts_cli_observer import TextsCLIObserver


@dataclass
class SnapshotCommands:
    create_snapshot_use_case: CreateSnapshotUseCase
    list_snapshots_use_case: ListSnapshotsUseCase
    restore_snapshot_use_case: RestoreSnapshotUseCase

    def create(self, args):
        texts_cli_observer = TextsCLIObserver()
        self.create_snapshot_use_case.subject.attach(texts_cli_observer)
        self.create_snapshot_use_case.execute(CreateSnapshotUseCaseDTO(
            name=args.name,
            description=args.description,
        ))

    def list(self, args):
        texts_cli_observer = TextsCLIObserver()
        snapshots_tree_cli_observer = SnapshotTreeCLIObserver()
        self.list_snapshots_use_case.subject.attach(texts_cli_observer)
        self.list_snapshots_use_case.subject.attach(snapshots_tree_cli_observer)

        self.list_snapshots_use_case.execute(ListSnapshotsUseCaseDTO())

    def restore(self, args):
        texts_cli_observer = TextsCLIObserver()
        select_option_cli_observer = SelectOptionCLIObserver()
        self.restore_snapshot_use_case.subject.attach(texts_cli_observer)
        self.restore_snapshot_use_case.subject.attach(select_option_cli_observer)

        self.restore_snapshot_use_case.execute(RestoreSnapshotUseCaseDTO(
            name=args.name,
        ))

    def delete(self, args):
        print("Deleting snapshot command")