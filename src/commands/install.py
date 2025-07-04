import os
import pprint
import sys
import time
from urllib.parse import urljoin

from colorama.ansi import Fore

from src import configuration
from src.texts.InstallTexts import InstallTexts
from src.utils.Utils import Utils
from src.utils.VboxManagerAdapter import VboxManagerAdapter
from src.utils.ConcurrentImporter import ConcurrentImporter


def run(args):
    cwd = os.getcwd()
    config = configuration.get_full_config(os.path.join(cwd, 'config.yaml'))

    ova_repo = config['storage']['ova']['repository']

    ova_dir = Utils.to_absolute_path(config['storage']['ova']['store_to'])
    vms_dir = Utils.to_absolute_path(config['storage']['virtual_machines']['store_to'])

    Utils.mkdirs(ova_dir, vms_dir)

    if not args.skip_download:
        InstallTexts.downloading_started()
        for vm in config['virtual_machines']:
            vm_name = vm['name']
            ova_url = urljoin(ova_repo, vm['ova_filename'])
            md5checksum = vm['md5checksum']
            download_path = os.path.join(ova_dir, f"{vm_name}.ova")
            download_needed = False

            if not os.path.exists(download_path):
                download_needed = True
            else:
                if not args.no_verify:
                    if md5checksum != Utils.calc_md5(download_path):
                        download_needed = True

            if download_needed:
                Utils.fetch_file(ova_url, download_path)
            else:
                InstallTexts.file_already_downloaded(vm_name)

    if not VboxManagerAdapter.create_nat_network():
        print(f"{Fore.RED} Unable to create NAT network")

    InstallTexts.importing_started()
    timestamp = int(time.time())
    concurrent_importer = ConcurrentImporter()
    for vm_name, filepath in Utils.find_files(ova_dir,".ova"):
        try:
            if os.path.exists(os.path.join(vms_dir, 'cyberlab',  vm_name)):
                InstallTexts.vm_already_exists(vm_name)
                continue

            concurrent_importer.import_vm(filepath, vm_name, vms_dir)

        except Exception as e:
            InstallTexts.error_importing_vm(vm_name, str(e))

    concurrent_importer.wait()

    for vm in config['virtual_machines']:
        vm_name = vm['name']

        if "nics" in vm:
            for nic in vm['nics']:
                if nic['type'] == "natnetwork":
                    VboxManagerAdapter.enable_nat_network(vm_name, nic['nic_index'], nic['name'])

    InstallTexts.all_operations_completed()
