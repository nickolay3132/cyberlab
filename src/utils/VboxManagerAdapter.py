import subprocess


class VboxManagerAdapter:
    @staticmethod
    def import_vm(ova_path: str, vm_name: str, vms_dir: str) -> bool:
        print(f"\nImporting {vm_name}...")
        cmd = [
            "vboxmanage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", vms_dir
        ]

        process = subprocess.Popen(cmd)
        process.wait()

        return process.returncode == 0