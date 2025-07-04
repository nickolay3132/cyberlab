import os

from src import configuration
from src.texts.ShutdownTexts import ShutdownTexts
from src.utils.VboxManagerAdapter import VboxManagerAdapter


def run(args):
    cwd = os.getcwd()

    vms = configuration.get_virtual_machines(os.path.join(cwd, "config.yaml"))

    for vm in vms:
        vm_name = vm['name']
        if args.force:
            ShutdownTexts.force_shutdown(vm_name)
            vm_shutdown_type = "poweroff"
        else:
            ShutdownTexts.shutdown(vm_name)
            vm_shutdown_type = vm['boot_policy']['shutdown']

        if not VboxManagerAdapter.stop_vm(vm_name, vm_shutdown_type):
            ShutdownTexts.failed_to_stop(vm_name)
