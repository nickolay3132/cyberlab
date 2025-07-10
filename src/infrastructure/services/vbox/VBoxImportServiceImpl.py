import os
import subprocess
from dataclasses import dataclass

from src.core.entities.ParrallelTask import ParallelTaskData
from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.services.ParallelTasksService import ParallelTasksService
from src.core.interfaces.services.vbox.VBoxImportService import VBoxImportService, ImportVMsDTO

@dataclass
class VBoxImportServiceImpl(VBoxImportService):
    output_handler: OutputHandler
    parallel_tasks_service: ParallelTasksService

    def import_vms(self, dto: ImportVMsDTO) -> None:
        for vm in dto.vms:
            ova_path = os.path.join(dto.ova_dir, f"{vm.name}.ova")
            log_file = os.path.join(dto.log_dir, f"{vm.name}.log")

            args = {
                'vm_name': vm.name,
                'ova_path': ova_path,
                'vms_dir': dto.vms_dir,
                'log_file': log_file
            }
            self.output_handler.text(f"Importing VM: {vm.name}")
            self.parallel_tasks_service.add_task(self._import_task, args=args)

        self.parallel_tasks_service.run()
        self.parallel_tasks_service.wait(self._check_import_task)

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
        if task_data.is_completed:
            self.output_handler.success(f"{task_data.args.get('vm_name')} successfully imported.")
        else:
            self.output_handler.show_error(f"Error importing {task_data.args.get('vm_name')}.")
            if task_data.error:
                self.output_handler.text(f"Reason: {task_data.error}")
            self.output_handler.text(f"Log file: {task_data.args.get('log_file')}")