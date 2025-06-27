import os
from urllib.parse import urljoin

from src import configuration
from src.utils.Utils import Utils
from src.utils.VboxManagerAdapter import VboxManagerAdapter


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
            Utils.fetch_file(ova_url, os.path.join(ova_dir, f"{vm_name}.ova"))

    print("\n=== IMPORTING VMS ===")
    for vm_name, filepath in Utils.find_files(ova_dir,".ova"):
        try:
            if os.path.exists(os.path.join(vms_dir, vm_name)):
                print(f"{vm_name} already imported! Skipping...")

            if not VboxManagerAdapter.import_vm(filepath, vm_name, vms_dir):
                print(f"\nError importing {vm_name}!")

        except Exception as e:
            print(f"\nError importing {vm_name}: {str(e)}")
    print("\nAll operations completed!")
