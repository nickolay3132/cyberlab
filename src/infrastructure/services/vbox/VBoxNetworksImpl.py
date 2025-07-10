import subprocess

from src.core.entities.VirtualMachine import VirtualMachine, Nic
from src.core.interfaces.services.vbox.VBoxNetworksService import VBoxNetworksService


class VBoxNetworksImpl(VBoxNetworksService):
    def create_nat_net(self) -> bool:
        nat_networks = subprocess.run(
            ["VBoxManage", "list", "natnetworks"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if not 'cyberlab' in nat_networks.stdout.lower():
            cmd = [
                "VBoxManage", "natnetwork", "add",
                "--netname", "cyberlab",
                "--network", "10.0.2.0/24",
                "--enable",
                "--dhcp", "on"
            ]

            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
            return process.returncode == 0
        else:
            return True

    def enable_nat_network(self, vm: VirtualMachine, nic: Nic) -> bool:
        cmd = [
            "VBoxManage", "modifyvm", vm.name,
            f"--nic{nic.index}", "natnetwork",
            f"--nat-network{nic.index}", nic.network_name,
            f"--cableconnected{nic.index}", "on"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        return process.returncode == 0