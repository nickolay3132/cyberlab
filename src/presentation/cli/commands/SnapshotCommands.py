from dataclasses import dataclass

from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCase, CreateSnapshotUseCaseDTO


@dataclass
class SnapshotCommands:
    create_snapshot_use_case: CreateSnapshotUseCase

    def create(self, args):
        self.create_snapshot_use_case.execute(CreateSnapshotUseCaseDTO(
            name=args.name,
            description=args.description,
        ))

    def list(self, args):
        print("Listing snapshots")

    def restore(self, args):
        print("Restoring snapshot command")

    def delete(self, args):
        print("Deleting snapshot command")