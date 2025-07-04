import os
import sys
import time

from src import configuration
from src.texts.snapshot.CreateTexts import CreateTexts
from src.utils.SnapshotsAdapter import SnapshotAdapter


def run(args):
    cwd = os.getcwd()
    config = configuration.get_full_config(os.path.join(cwd, 'config.yaml'))
    vm_names = [vm['name'] for vm in config['virtual_machines']]
    timestamp = int(time.time())

    # if args.vm != "":
    #     vm_name = args.vm
    #     if not vm_name in vm_names:
    #         CreateTexts.vm_not_exist(vm_name)
    #         sys.exit(1)
    #
    #     SnapshotAdapter.create(vm_name, snapshot_name, args.description)
    # else:
    for vm_name in vm_names:
        SnapshotAdapter.create(vm_name, f"{timestamp}-{args.name}", args.description)