import os

from src import configuration
from src.utils.Utils import Utils
from src.utils.VboxManagerAdapter import VboxManagerAdapter


def run(args):
    cwd = os.getcwd()
    vms = configuration.get_vms(os.path.join(cwd, 'vms.cfg'))

    Utils.mkdirs(os.path.join(cwd, 'ova'), os.path.join(cwd, 'vms'))

    if not args.skip_fetching:
        print("\n=== DOWNLOADING VMS ===")
        for vm in vms:
            vm_name, ova_url = vm
            Utils.fetch_file(ova_url, os.path.join(cwd, 'ova', f"{vm_name}.ova"))

    print("\n=== IMPORTING VMS ===")
    for vm_name, filepath in Utils.find_files(os.path.join(cwd, 'ova'),".ova"):
        try:
            if os.path.exists(os.path.join(cwd,"vms", vm_name)):
                print(f"{vm_name} already imported! Skipping...")

            if not VboxManagerAdapter.import_vm(filepath, vm_name, os.path.join(cwd, 'vms')):
                print(f"\nError importing {vm_name}!")

        except Exception as e:
            print(f"\nError importing {vm_name}: {str(e)}")
    print("\nAll operations completed!")
