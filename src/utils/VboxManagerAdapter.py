import subprocess
import threading
import os
import time

from typing import Literal

class ConcurrentImporter:
    results = [None] * 100
    errors = [None] * 100
    names = [None] * 100
    tasks = [None] * 100

    count = 0

    @staticmethod
    def import_vm(ova_path: str, vm_name: str, vms_dir: str) -> bool:
        id = ConcurrentImporter.count
        ConcurrentImporter.count += 1
        def handler(ova_paht, vm_name, vms_dir):
            try:
                VboxManagerAdapter.import_vm(ova_path, vm_name, vms_dir)
            except Exception as e:
                results[id] = False
                errors[id] = e
            else:
                results[id] = True
            finally:
                return

        thread = threading.Thread(target=handler,
                         args=(ova_path, vm_name, vms_dir))
        ConcurrentImporter.names[id] = vm_name
        ConcurrentImporter.tasks[id] = thread
        ConcurrentImporter.tasks[id].start()

    @staticmethod
    def wait():
        # removing empty stuff
        ConcurrentImporter.results = list(filter((None).__ne__, ConcurrentImporter.results))
        ConcurrentImporter.names = list(filter((None).__ne__, ConcurrentImporter.names))
        ConcurrentImporter.tasks = list(filter((None).__ne__, ConcurrentImporter.tasks))

        name_buf = ConcurrentImporter.names
        task_buf = ConcurrentImporter.tasks
        while ConcurrentImporter.count != 0:
            for index, task in enumerate(ConcurrentImporter.tasks):
                if task.is_alive() == False:
                    print("*** {:^60} ***".format(f"{ConcurrentImporter.names[index]} finished importing!"))
                    del ConcurrentImporter.tasks[index]
                    del ConcurrentImporter.names[index]
                    ConcurrentImporter.count -= 1
                    break

                # so we don't use CPU for nothing
                time.sleep(0.25)
                   
        ConcurrentImporter.names = name_buf
        ConcurrentImporter.tasks = task_buf

class VboxManagerAdapter:
    @staticmethod
    def import_vm(ova_path: str, vm_name: str, vms_dir: str) -> bool:
        print(f"\nImporting {vm_name}...")
        cmd = [
            "VBoxManage", "import", ova_path,
            "--vsys", "0",
            "--vmname", vm_name,
            "--group", "/cyberlab",
            "--options", "keepallmacs",
            "--basefolder", vms_dir
        ]

        if not os.path.exists('import_log'):
            os.makedirs('import_log')

        log_file_name = os.path.join('import_log', f'{vm_name}.log')
        log_file = open(log_file_name, "w")

        process = subprocess.Popen(cmd, stdout=log_file, stderr=log_file)
        process.wait()

        return process.returncode == 0

    @staticmethod
    def start_vm(vm_name: str, launch_type: Literal["gui", "headless", "separate"] = "gui") -> bool:
        cmd = [
            "VBoxManage", "startvm", vm_name, "--type", launch_type,
        ]

        process = subprocess.Popen(cmd)
        process.wait()
        return process.returncode == 0

    @staticmethod
    def stop_vm(vm_name: str, shutdown_type: Literal["acpipowerbutton", "poweroff", "savestate"]) -> bool:
        print(f"\nStopping {vm_name}...")
        cmd = [
            "VBoxManage", "controlvm", vm_name, shutdown_type
        ]

        process = subprocess.Popen(cmd)
        process.wait()

        return process.returncode == 0

