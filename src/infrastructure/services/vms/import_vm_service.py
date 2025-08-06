from typing import Tuple, Callable

from src.core.entities import VM, ParallelTask
from src.core.interfaces.gateways.vms_gateway import IVMsGateway
from src.core.interfaces.services import IFileSystemService, IParallelTaskService
from src.core.interfaces.services.vms import IImportVMService


class ImportVMServiceImpl(IImportVMService):
    def __init__(self,
                 file_system_servie: IFileSystemService,
                 parallel_task_service: IParallelTaskService,
                 vms_gateway: IVMsGateway,
                 ):
        self.file_system_service = file_system_servie
        self.parallel_task_service = parallel_task_service

        self.vms_gateway = vms_gateway

        self.callback = lambda _, __: None

    def set_callback(self, callback: Callable[[str, bool], None]) -> None:
        self.callback = callback

    def prepare_storage(self, ova_store_to: str, vms_store_to: str, log_store_to: str) -> Tuple[str, str, str]:
        absolute_ova_path = self.file_system_service.to_absolute_path(ova_store_to)
        absolute_vms_path = self.file_system_service.to_absolute_path(vms_store_to)
        absolute_log_path = self.file_system_service.to_absolute_path(log_store_to)
        self.file_system_service.mkdirs(absolute_vms_path, absolute_log_path, ova_store_to)
        return absolute_ova_path, absolute_vms_path, absolute_log_path

    def import_vm(self, vm: VM, ova_dir: str, vms_dir: str, log_dir: str) -> None:
        ova_path = f"{ova_dir}/{vm.name}.ova"
        log_path = f"{log_dir}/{vm.name}.log"

        args = {
            'vm_name': vm.name,
            'ova_path': ova_path,
            'vms_dir': vms_dir,
            'log_path': log_path,
        }

        self.parallel_task_service.add_task(self._import_task, args)

    def run(self):
        self.parallel_task_service.run()
        self.parallel_task_service.wait(self._check_import_task)

    def _import_task(self, task: ParallelTask) -> None:
        ova_path = task.args['ova_path']
        vm_name = task.args['vm_name']
        vms_dir = task.args['vms_dir']
        log_path = task.args['log_path']

        try:
            with open(log_path, 'w') as log:
                return_code = self.vms_gateway.import_vm(ova_path, vm_name, vms_dir, log)

                with task.thread_lock:
                    if return_code == 0:
                        task.is_completed = True
                    else:
                        task.is_completed = False
                        task.error = f"Failed to import {vm_name}"

        except Exception as e:
            with open (log_path, 'a') as log:
                log.write(f"Exception during import: {str(e)}\n")
            with task.thread_lock:
                task.is_completed = False
                task.error = str(e)

    def _check_import_task(self, task: ParallelTask) -> None:
        self.callback(task.args['vm_name'], task.is_completed)