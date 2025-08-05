from typing import List

from src.core.entities.VirtualMachine import VirtualMachine, Nic, BootPolicy
from src.core.exceptions.VirtualMachineNotFound import VirtualMachineNotFoundError, VirtualMachineNotFound
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.infrastructure.repositories.common.YamlLoader import YamlLoader


class VirtualMachinesRepositoryImpl(VirtualMachinesRepository):
    def __init__(self, yaml_loader: YamlLoader):
        self.data = yaml_loader.read().get("virtual_machines", [])

    def get_all(self) -> List[VirtualMachine]:
        return [ self._get_vm_instance(vm) for vm in self.data ]

    def get_by_name(self, name: str) -> VirtualMachine:
        found_vm = None
        for vm in self.get_all():
            if vm.name == name:
                found_vm = vm

        if found_vm is None:
            raise VirtualMachineNotFoundError(VirtualMachineNotFound(
                message="Virtual machine not found",
                vm_name=name
            ))

        return found_vm


    def _get_vm_instance(self, vm: dict) -> VirtualMachine:
        return VirtualMachine(
            name=vm.get("name"),
            ova_filename=vm.get("ova_filename"),
            md5checksum=vm.get("md5checksum", ""),
            nics=[ self._get_nic_instance(nic) for nic in vm.get("nics", []) ],
            boot_policy=BootPolicy(
                startup=vm.get("boot_policy", {}).get("startup", "gui"),
                shutdown=vm.get("boot_policy", {}).get("shutdown", "acpipowerbutton"),
            )
        )

    @staticmethod
    def _get_nic_instance(nic: dict) -> Nic:
        return Nic(
            index=nic.get("nic_index", 1),
            type=nic.get("type", "intnetwork"),
            network_name=nic.get("network_name"),
        )