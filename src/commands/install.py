import os
from urllib.parse import urljoin

from src import configuration
from src.texts.InstallTexts import InstallTexts
from src.utils.Utils import Utils
from src.utils.VboxManagerAdapter import VboxManagerAdapter


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

    InstallTexts.importing_started()
    for vm_name, filepath in Utils.find_files(ova_dir,".ova"):
        try:
            if os.path.exists(os.path.join(vms_dir, vm_name)):
                InstallTexts.vm_already_exists(vm_name)

            if not VboxManagerAdapter.import_vm(filepath, vm_name, vms_dir):
                InstallTexts.error_importing_vm(vm_name)

        except Exception as e:
            InstallTexts.error_importing_vm(vm_name, str(e))

    InstallTexts.all_operations_completed()
