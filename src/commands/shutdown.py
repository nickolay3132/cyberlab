import os

from src import configuration
from src.utils.Utils import Utils
from src.utils.VboxManagerAdapter import VboxManagerAdapter


def run(args):
    Utils.print_cli_hello()

    cwd = os.getcwd()

    vms = configuration.get_virtual_machines(os.path.join(cwd, "config.yaml"))

    for vm in vms:
        vm_name = vm['name']
        vm_shutdown_type = vm['boot_policy']['shutdown']

        if not VboxManagerAdapter.stop_vm(vm_name, vm_shutdown_type):
            print(f"Failed to stop virtual machine {vm_name}")
