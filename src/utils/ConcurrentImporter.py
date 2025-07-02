import subprocess
import threading
import time
import os
from dataclasses import dataclass
from typing import List

from src.utils.VboxManagerAdapter import VboxManagerAdapter


@dataclass
class ImportVmTask:
    vm_name: str
    is_completed: bool = False
    thread: threading.Thread = None
    error: str = None


class ConcurrentImporter:
    def __init__(self, log_dir: str = "import_log"):
        self._tasks: List[ImportVmTask] = []
        self._lock = threading.Lock()
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def import_vm(self, ova_path: str, vm_name: str, vms_dir: str):
        thread = threading.Thread(
            target=self._thread_handler,
            args=(ova_path, vm_name, vms_dir),
            daemon=True
        )

        with self._lock:
            task = ImportVmTask(
                vm_name=vm_name,
                thread=thread,
            )
            self._tasks.append(task)

        thread.start()

    def wait(self):
        while True:
            with self._lock:
                if not self._tasks:
                    break

                completed_tasks = [t for t in self._tasks if not t.thread.is_alive()]

                for task in completed_tasks:
                    self._check_task(task)
                    self._tasks.remove(task)

            time.sleep(0.25)

    def _check_task(self, task: ImportVmTask):
        if task.is_completed:
            print("***" + f"{task.vm_name} successfully imported.".center(60) + "***")
        else:
            print(f"\nError importing {task.vm_name}")
            if task.error:
                print(f"Reason: {task.error}")
            print(f"Log file: {os.path.join(self.log_dir, f'{task.vm_name}.log')}")

    def _thread_handler(self, ova_path: str, vm_name: str, vms_dir: str):
        log_file = os.path.join(self.log_dir, f"{vm_name}.log")

        try:
            with self._lock:
                task = next(t for t in self._tasks if t.vm_name == vm_name)

            success = VboxManagerAdapter.import_vm(ova_path, vm_name, vms_dir, log_file)

            with self._lock:
                task.is_completed = success

        except Exception as e:
            with self._lock:
                task.is_completed = False
                task.error = str(e)
            with open(log_file, "a") as f:
                f.write(f"Critical error: {str(e)}\n")