import os
import subprocess
import requests
from tqdm import tqdm


def download_file(url, filename):
    print(f"\nDownloading {os.path.basename(filename)}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192

    with open(filename, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                pbar.update(len(chunk))


def import_vm(ova_path, vm_name, vms_dir):
    print(f"\nImporting {vm_name}...")
    cmd = [
        "vboxmanage", "import", ova_path,
        "--vsys", "0",
        "--vmname", vm_name,
        "--group", "/cyberlab",
        "--options", "keepallmacs",
        "--basefolder", vms_dir
    ]

    process = subprocess.Popen(cmd)
    process.wait()

    return process.returncode == 0

def main():
    project_root = os.getcwd()

    ova_dir = os.path.join(project_root, "ova")
    vms_dir = os.path.join(project_root, "vms")

    if not os.path.exists(ova_dir):
        os.makedirs(ova_dir)
    if not os.path.exists(vms_dir):
        os.makedirs(vms_dir)

    vms = [
        ['firewall-1', 'https://files.techno-cyber-lab.store/fw1-pfsense.ova'],
        ['firewall-2', 'https://files.techno-cyber-lab.store/fw2-pfsense.ova'],
        ['web-server', 'https://files.techno-cyber-lab.store/dmz-serv.ova'],
        ['database-server', 'https://files.techno-cyber-lab.store/db-serv.ova'],
        ['wan-client', 'https://files.techno-cyber-lab.store/kali-client.ova'],
        ['lan-client', 'https://files.techno-cyber-lab.store/kali-lan-client.ova']
    ]

    print("\n=== DOWNLOADING VMS ===")
    import_queue = []
    for vm in vms:
        vm_name, ova_url = vm

        try:
            ova_filename = os.path.join(ova_dir, f"{vm_name}.ova")
            import_queue.append((vm_name, ova_url, ova_filename))

            if os.path.exists(ova_filename):
                print(f"{os.path.basename(ova_filename)} already exists! Skipping...")
                continue

            download_file(ova_url, ova_filename)

        except Exception as e:
            print(f"\nError processing vm: {vm_name}\n{str(e)}")


    print("\n=== IMPORTING VMS ===")
    for vm_name, ova_url, ova_filename in import_queue:
        try:
            if not os.path.exists(ova_filename):
                print(f"\nError: OVA file {os.path.basename(ova_filename)} not found! Skipping {vm_name}")
                continue

            if os.path.exists(os.path.join(vms_dir, vm_name)):
                print(f"{vm_name} already imported! Skipping...")

            if not import_vm(ova_filename, vm_name, vms_dir):
                print(f"\nError importing {vm_name}!")

        except Exception as e:
            print(f"\nError importing {vm_name}: {str(e)}")

    print("\nAll operations completed!")

if __name__ == "__main__":
    main()