from src.bootstrap.binder import bind
from src.core.interfaces.gateways import IVMsGateway, IVmsNetworkGateway
from src.infrastructure.gateways import VmsGatewayImpl, VmsNetworkGatewayImpl


@bind
def make_vms_gateway() -> IVMsGateway:
    return VmsGatewayImpl()

@bind
def make_vms_network_gateway() -> IVmsNetworkGateway:
    return VmsNetworkGatewayImpl()