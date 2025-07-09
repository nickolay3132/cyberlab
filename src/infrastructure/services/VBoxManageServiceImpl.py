import os.path
import subprocess
import sys
from typing import Tuple

from src.core.entities.ParrallelTask import ParallelTaskData
from src.core.entities.VirtualMachine import VirtualMachine
from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.FileSystemService import FileSystemService
from src.core.interfaces.services.ParallelTasksService import ParallelTasksService
from src.core.interfaces.services.VBoxManageService import VBoxManageService
from src.core.interfaces.services.VBoxNetworksService import VBoxNetworksService


class VBoxManageServiceImpl (VBoxManageService):
    def __init__(self,
                 storage_repository: StorageRepository,
                 virtual_machines_repository: VirtualMachinesRepository,
                 file_system_service: FileSystemService,
                 vbox_networks_service: VBoxNetworksService,
                 parallel_tasks_service: ParallelTasksService,
                 output_handler: OutputHandler):
        self.storage_repository = storage_repository
        self.virtual_machines_repository = virtual_machines_repository
        self.file_system_service = file_system_service
        self.vbox_networks_service = vbox_networks_service
        self.parallel_tasks_service = parallel_tasks_service
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

            args = {
                'vm_name': vm.name,
                'ova_path': ova_path,
                'vms_dir': vms_dir,
                'log_file': log_file
            }
            self.output_handler.text(f"Importing VM: {vm.name}")
            self.parallel_tasks_service.add_task(self._import_task, args=args)

        self.parallel_tasks_service.run()
        self.parallel_tasks_service.wait(self._check_import_task)
        return None

    def enable_networks(self) -> None:
        for vm in self.virtual_machines_repository.get_all():
            for nic in vm.nics:
                if nic.type == "natnetwork":
                    self.vbox_networks_service.enable_nat_network(vm, nic)

    def networks(self) -> VBoxNetworksService:
        return self.vbox_networks_service

    @staticmethod
    def _import_task(task_data: ParallelTaskData) -> None:
        cmd = [
            "VBoxManage", "import", task_data.args.get('ova_path'),
            "--vsys", "0",
            "--vmname", task_data.args.get('vm_name'),
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", task_data.args.get('vms_dir'),
        ]

        try:
            with open(task_data.args.get('log_file'), "w") as log:
                log.write(f"Starting import of {task_data.args.get('vm_name')} from {task_data.args.get('ova_path')}\n")

                process = subprocess.Popen(
                    cmd,
                    stdout=log,
                    stderr=log,
                    text=True,
                    encoding="utf-8"
                )

                process.wait()

                with task_data.thread_lock:
                    if process.returncode == 0:
                        task_data.is_completed = True
                    else:
                        task_data.is_completed = False
                        task_data.error = f"Failed to import {task_data.args.get('vm_name')}."

        except Exception as e:
            with open(task_data.args.get('log_file'), "a") as log:
                log.write(f"Exception during import: {str(e)}\n")
            with task_data.thread_lock:
                task_data.is_completed = False
                task_data.error = str(e)

    def _check_import_task(self, task_data: ParallelTaskData) -> None:
        if task_data.is_completed:
            self.output_handler.success(f"{task_data.args.get('vm_name')} successfully imported.")
        else:
            self.output_handler.show_error(f"Error importing {task_data.args.get('vm_name')}.")
            if task_data.error:
                self.output_handler.text(f"Reason: {task_data.error}")
            self.output_handler.text(f"Log file: {task_data.args.get('log_file')}")