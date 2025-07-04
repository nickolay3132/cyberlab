import os

from colorama.ansi import Fore

from src import configuration
from src.utils.SnapshotsAdapter import SnapshotAdapter
from src.utils.SnapshotsSelector import SnapshotSelector


def run(args):
    cwd = os.getcwd()
    config = configuration.get_full_config(os.path.join(cwd, 'config.yaml'))
    vm_names = [vm['name'] for vm in config['virtual_machines']]

    selector = SnapshotSelector.find_all_snapshots(vm_names)
    selected_snapshots = selector.select_for_all_vms(args.name)

    for vm_name, snapshot in selected_snapshots.items():
        if snapshot:
            print(f"{Fore.GREEN}Restoring VM {vm_name} to snapshot {snapshot.name}")
            SnapshotAdapter.restore(vm_name, f"{snapshot.timestamp}-{snapshot.name}")
