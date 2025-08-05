from typing import List, Optional

from src.core.entities import VM, BootPolicy, Nic
from src.core.enums import BootPolicyStartupType, BootPolicyShutdownType, NicType
from src.core.interfaces.repositories import IVMRepository
from src.infrastructure.repositories import YamlLoader


class YamlVmRepository(IVMRepository):
    def __init__(self, yaml_loader: YamlLoader):
        self.data = yaml_loader.read().get("virtual_machines", [])

    def get_all(self) -> List[VM]:
        return [ self._get_vm_instance(vm) for vm in self.data ]

    def get_by_name(self, name: str) -> Optional[VM]:
        found_vm = None
        for vm in self.get_all():
            if vm.name == name:
                found_vm = vm

        return found_vm


    def _get_vm_instance(self, vm: dict) -> VM:
        vm_boot_policy: dict = vm.get("boot_policy", {})
        return VM(
            name=vm.get("name"),
            ova_filename=vm.get("ova_filename"),
            md5checksum=vm.get("md5checksum", ""),
            nics=[ self._get_nic_instance(nic) for nic in vm.get("nics", []) ],
            boot_policy=BootPolicy(
                startup=BootPolicyStartupType(vm_boot_policy.get("startup", 'gui')),
                shutdown=BootPolicyShutdownType(vm_boot_policy.get("shutdown", 'acpipowerbutton')),
            )
        )

    @staticmethod
    def _get_nic_instance(nic: dict) -> Nic:
        return Nic(
            index=nic.get("nic_index", 1),
            type=NicType(nic.get("type", "intnetwork")),
            network_name=nic.get("network_name"),
        )