import subprocess


class SnapshotAdapter:
    @staticmethod
    def create(vm_name: str, snapshot_name: str, description: str = "") -> None:
        cmd = [
            "VBoxManage", "snapshot", vm_name,
            "take", snapshot_name,
            "--description", description,
        ]

        process = subprocess.Popen(cmd)
        process.wait()
        print()
        return None