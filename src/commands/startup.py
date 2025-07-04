import os.path

from src import configuration
from src.texts.StartupTexts import StartupTexts
from src.utils.VboxManagerAdapter import VboxManagerAdapter


def run(args):
    cwd = os.getcwd()
    vms = configuration.get_virtual_machines(os.path.join(cwd, "config.yaml"))

    for vm in vms:
        vm_name = vm['name']
        vm_startup_type = vm['boot_policy']['startup']

        if not VboxManagerAdapter.start_vm(vm_name, vm_startup_type):
            StartupTexts.failed_to_start(vm_name)
