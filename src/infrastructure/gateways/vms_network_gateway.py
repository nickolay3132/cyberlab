import subprocess

from src.core.interfaces.gateways import IVmsNetworkGateway


class VmsNetworkGatewayImpl(IVmsNetworkGateway):
    def get_nat_networks_str(self) -> str:
        nat_networks = subprocess.run(
            ["VBoxManage", "list", "natnetworks"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        return nat_networks.stdout

    def create_nat_network(self, net_name: str, network: str, enable_dhcp: bool = False) -> bool:
        cmd = [
            "VBoxManage", "natnetwork", "add",
            "--netname", net_name,
            "--network", network,
            "--enable",
        ]

        if enable_dhcp:
            cmd.extend(["--dhcp", "on"])

        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        return process.returncode == 0

    def enable_nat_nic(self, vm_name: str, nic_index: int, net_name: str) -> bool:
        cmd = [
            "VBoxManage", "modifyvm", vm_name,
            f"--nic{nic_index}", "natnetwork",
            f"--nat-network{nic_index}", net_name,
            f"--cableconnected{nic_index}", "on"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        return process.returncode == 0