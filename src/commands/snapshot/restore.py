import os

from colorama.ansi import Fore

from src import configuration
from src.utils.SnapshotsAdapter import SnapshotAdapter
from src.utils.SnapshotsSelector import SnapshotSelector
from src.utils.SnapshotsTree import SnapshotsTree, SnapshotData


def run(args):
    cwd = os.getcwd()
    config = configuration.get_full_config(os.path.join(cwd, 'config.yaml'))
    vm_names = [vm['name'] for vm in config['virtual_machines']]
    all_snapshots: dict[str, list[SnapshotData]] = {}

    for vm_name in vm_names:
        vm_snapshots = SnapshotAdapter.list(vm_name)
        snapshots_list = SnapshotsTree(vm_snapshots).get_list()
        all_snapshots.update({vm_name: snapshots_list})

    selector = SnapshotSelector(all_snapshots)
    selected_snapshots = selector.select_for_all_vms(args.name)

    for vm_name, snapshot in selected_snapshots.items():
        if snapshot:
            print(f"{Fore.GREEN}Restoring VM {vm_name} to snapshot {snapshot.name}")
            SnapshotAdapter.restore(vm_name, f"{snapshot.timestamp}-{snapshot.name}")
