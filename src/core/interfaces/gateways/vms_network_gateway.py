from abc import ABC, abstractmethod


class IVmsNetworkGateway(ABC):
    @abstractmethod
    def get_nat_networks_str(self) -> str: pass

    @abstractmethod
    def create_nat_network(self, net_name: str, network: str, enable_dhcp: bool = False) -> bool: pass

    @abstractmethod
    def enable_nat_nic(self, vm_name: str, nic_index: int, net_name: str) -> bool: pass