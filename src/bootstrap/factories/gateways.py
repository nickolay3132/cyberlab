from src.bootstrap.binder import bind
from src.core.interfaces.gateways import IVMsGateway
from src.infrastructure.gateways import VmsGatewayImpl


@bind
def make_vms_gateway() -> IVMsGateway:
    return VmsGatewayImpl()