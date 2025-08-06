from dataclasses import dataclass

from src.core.enums import BootPolicyShutdownType, BootPolicyStartupType
from src.core.interfaces.gateways import IVmsBootGateway
from src.core.interfaces.services.vms import IVmBootService

@dataclass
class VmBootServiceImpl(IVmBootService):
    vms_boot_gateway: IVmsBootGateway
    
    def startup(self, vm_name: str, startup_boot_policy: BootPolicyStartupType) -> bool:
        return self.vms_boot_gateway.startup(vm_name, startup_boot_policy.value)

    def shutdown(self, vm_name: str, shutdown_boot_policy: BootPolicyShutdownType, force: bool = False) -> bool:
        if force:
            return self.vms_boot_gateway.shutdown(vm_name, BootPolicyShutdownType.POWER_OFF.value)

        return self.vms_boot_gateway.shutdown(vm_name, shutdown_boot_policy.value)