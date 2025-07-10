from dataclasses import dataclass


@dataclass
class SnapshotCommands:
    def create(self):
        print("Creating snapshot command")

    def list(self):
        print("Listing snapshots")

    def restore(self):
        print("Restoring snapshot command")

    def delete(self):
        print("Deleting snapshot command")