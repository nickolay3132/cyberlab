import os.path
import subprocess
import sys

from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.FileSystemService import FileSystemService
from src.core.interfaces.services.VBoxManageService import VBoxManageService


class VBoxManageServiceImpl (VBoxManageService):
    def __init__(self,
                 storage_repository: StorageRepository,
                 virtual_machines_repository: VirtualMachinesRepository,
                 file_system_service: FileSystemService,
                 output_handler: OutputHandler):
        self.storage_repository = storage_repository
        self.virtual_machines_repository = virtual_machines_repository
        self.file_system_service = file_system_service
        self.output_handler = output_handler

    def import_vms(self) -> None:
        storage = self.storage_repository.get()
        log_dir = self.file_system_service.to_absolute_path(storage.import_log_store_to)
        vms_dir = self.file_system_service.to_absolute_path(storage.vms_store_to)
        ova_path = self.file_system_service.to_absolute_path(storage.ova_store_to)

        self.file_system_service.mkdirs(log_dir, vms_dir)

        self.output_handler.space()
        self.output_handler.show("Importing VMS")

        for vm in self.virtual_machines_repository.get_all():
            ova_path = os.path.join(ova_path, f"{vm.name}.ova")
            log_file = os.path.join(log_dir, f"{vm.name}.log")

            cmd = [
                "VBoxManage", "import", ova_path,
                "--vsys", "0",
                "--vmname", vm.name,
                "--group", "/cyberlab",
                "--options", "keepallmacs",
                "--basefolder", vms_dir
            ]

            self.output_handler.text(f"Importing VM: {vm.name}")
            try:
                with open(log_file, "w") as log:
                    log.write(f"Starting import of {vm.name} from {ova_path}\n")

                    process = subprocess.Popen(
                        cmd,
                        stdout=log,
                        stderr=log,
                        text=True,
                        encoding="utf-8"
                    )

                    process.wait()

                    if process.returncode == 0:
                        self.output_handler.success(f"{vm.name} successfully imported")
                    else:
                        self.output_handler.show_error(f"{vm.name} failed to import. Log file: {log_file}")

            except Exception as e:
                with open(log_file, "a") as log:
                    log.write(f"Exception during import: {str(e)}\n")
                self.output_handler.show_error(f"{vm.name} failed to import. Log file: {log_file}")

        return None