from typing import Optional

from src.core.entities import VM, Nic
from src.core.interfaces.gateways import IVmsNetworkGateway
from src.core.interfaces.services.vms import IVmNetworkService


class VmNetworkServiceImpl(IVmNetworkService):
    def __init__(self, vms_network_gateway: IVmsNetworkGateway):
        self.vms_network_gateway = vms_network_gateway

    def enable_vm_nics(self, vm: VM) -> bool:
        is_success = True

        for nic in vm.nics:
            match nic.type:
                case "natnetwork":
                    is_success = self._enable_nat_network(vm.name, nic)

        return is_success

    def _enable_nat_network(self, vm_name: str, nic: Nic) -> bool:
        net_created: Optional[bool] = None
        if nic.network_name not in self.vms_network_gateway.get_nat_networks_str():
            net_created = self.vms_network_gateway.create_nat_network(nic.network_name, '10.0.2.0/24', True)

        if net_created is None or net_created:
            self.vms_network_gateway.enable_nat_nic(vm_name, nic.index, nic.network_name)
            return True

        return False
