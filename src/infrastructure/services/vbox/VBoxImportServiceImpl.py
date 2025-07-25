import os
import subprocess
from dataclasses import dataclass
from typing import Optional

from src.core.entities.ParrallelTask import ParallelTaskData
from src.core.entities.observer import Subject, ObserverEvent
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.core.interfaces.services.FileSystemService import FileSystemService
from src.core.interfaces.services.ParallelTasksService import ParallelTasksService
from src.core.interfaces.services.vbox.VBoxImportService import VBoxImportService

@dataclass
class VBoxImportServiceImpl(VBoxImportService):
    parallel_tasks_service: ParallelTasksService
    file_system_service: FileSystemService

    storage_repository: StorageRepository
    virtual_machines_repository: VirtualMachinesRepository

    log_dir: Optional[str] = None
    vms_dir: Optional[str] = None
    ova_dir: Optional[str] = None

    subject: Optional[Subject] = None

    def import_vms(self, subject: Subject) -> None:
        self.prepare_storage()
        self.subject = subject

        subject.notify(ObserverEvent.space(id='main'))
        subject.notify(ObserverEvent.title(id='main', data='Importing VMS'))

        for vm in self.virtual_machines_repository.get_all():
            ova_path = os.path.join(self.ova_dir, f"{vm.name}.ova")
            log_file = os.path.join(self.log_dir, f"{vm.name}.log")

            args = {
                'vm_name': vm.name,
                'ova_path': ova_path,
                'vms_dir': self.vms_dir,
                'log_file': log_file
            }
            subject.notify(ObserverEvent.text(id=vm.name, data=f"Importing VM: {vm.name}"))
            self.parallel_tasks_service.add_task(self._import_task, args=args)

        self.parallel_tasks_service.run()
        self.parallel_tasks_service.wait(self._check_import_task)

    def prepare_storage(self) -> None:
        storage = self.storage_repository.get()
        self.log_dir = self.file_system_service.to_absolute_path(storage.import_log_store_to)
        self.vms_dir = self.file_system_service.to_absolute_path(storage.vms_store_to)
        self.ova_dir = self.file_system_service.to_absolute_path(storage.ova_store_to)

        self.file_system_service.mkdirs(self.log_dir, self.vms_dir)

    @staticmethod
    def _import_task(task_data: ParallelTaskData) -> None:
        ova_path = task_data.args.get('ova_path')
        vm_name = task_data.args.get('vm_name')
        vms_dir = task_data.args.get('vms_dir')
        log_file = task_data.args.get('log_file')

        cmd = [
            "VBoxManage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", vms_dir,
        ]

        try:
            with open(log_file, "w") as log:
                log.write(f"Starting import of {vm_name} from {ova_path}\n")

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
            with open(log_file, "a") as log:
                log.write(f"Exception during import: {str(e)}\n")
            with task_data.thread_lock:
                task_data.is_completed = False
                task_data.error = str(e)

    def _check_import_task(self, task_data: ParallelTaskData) -> None:
        vm_name = task_data.args.get('vm_name')

        if task_data.is_completed:
            self.subject.notify(ObserverEvent.success(id=vm_name, data=f"{vm_name} successfully imported."))
        else:
            self.subject.notify(ObserverEvent.error(id=vm_name, data=f"{vm_name} failed to import."))
            self.subject.notify(ObserverEvent.text(id='main', data=f"Log files at {self.log_dir}"))
            # if task_data.error:
            #     self.subject.notify(ObserverEvent.error(
            #         id='main',
            #         data=f"Reason for failure importing {vm_name}: {task_data.error}"
            #     ))
            # self.subject.notify(ObserverEvent.text(id='main', data=f"Log file: {task_data.args.get('log_file')}"))