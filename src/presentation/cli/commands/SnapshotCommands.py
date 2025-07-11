from dataclasses import dataclass


@dataclass
class SnapshotCommands:
    def create(self, args):
        print("Creating snapshot command")

    def list(self, args):
        print("Listing snapshots")

    def restore(self, args):
        print("Restoring snapshot command")

    def delete(self, args):
        print("Deleting snapshot command")