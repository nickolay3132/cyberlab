import os
import time
from urllib.parse import urljoin

from src import configuration
from src.utils.Utils import Utils
# from src.utils.VboxManagerAdapter import VboxManagerAdapter
from src.utils.VboxManagerAdapter import ConcurrentImporter

import threading

def run(args):
    Utils.print_cli_hello()

    cwd = os.getcwd()
    config = configuration.get_full_config(os.path.join(cwd, 'config.yaml'))

    ova_repo = config['storage']['ova']['repository']

    ova_dir = Utils.to_absolute_path(config['storage']['ova']['store_to'])
    vms_dir = Utils.to_absolute_path(config['storage']['virtual_machines']['store_to'])

    Utils.mkdirs(ova_dir, vms_dir)

    if not args.skip_fetching:
        print("\n=== DOWNLOADING VMS ===")
        for vm in config['virtual_machines']:
            vm_name = vm['name']
            ova_url = urljoin(ova_repo, vm['ova_filename'])
    
            ova_file = os.path.join(ova_dir, f"{vm_name}.ova")
            Utils.fetch_file(ova_url, ova_file, args.check_existing)

    print("\n=== IMPORTING VMS ===")

    for vm_name, filepath in Utils.find_files(ova_dir,".ova"):
        try:
            if os.path.exists(os.path.join(vms_dir, vm_name)):
                print(f"{vm_name} already imported! Skipping...")

            ConcurrentImporter.import_vm(filepath, vm_name, vms_dir)

        except Exception as e:
            print(f"\nError importing {vm_name}: {str(e)}")

    ConcurrentImporter.wait()

    for index, result in enumerate(ConcurrentImporter.results):
        if result == False:
            print("\nError importing {name}: {err}"
                  .format(ConcurrentImporter.names[index],
                          ConcurrentImporter.errors[index]))

    print("\nAll operations completed!")
