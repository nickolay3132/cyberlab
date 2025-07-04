import os

from colorama.ansi import Fore

from src import configuration
from src.utils.SnapshotsAdapter import SnapshotAdapter
from src.utils.SnapshotsTree import SnapshotsTree


def run(args):
    cwd = os.getcwd()
    config = configuration.get_full_config(os.path.join(cwd, 'config.yaml'))
    vm_names = [vm['name'] for vm in config['virtual_machines']]

    for vm_name in vm_names:
        try:
            snapshots = SnapshotAdapter.list(vm_name)
            tree = SnapshotsTree(snapshots)

            print(f"{Fore.CYAN}{vm_name} snapshots tree:")
            tree.print()
            print()
        except Exception as e:
            print(e)


