from src.bootstrap.binder import bind
from src.core.interfaces.gateways import IVMsGateway, IVmsNetworkGateway, IVmsBootGateway, IVmsSnapshotsGateway
from src.infrastructure.gateways import VmsGatewayImpl, VmsNetworkGatewayImpl, VmsBootGatewayImpl, VmsSnapshotsGateway


@bind
def make_vms_gateway() -> IVMsGateway:
    return VmsGatewayImpl()

@bind
def make_vms_network_gateway() -> IVmsNetworkGateway:
    return VmsNetworkGatewayImpl()

@bind
def make_vms_boot_gateway() -> IVmsBootGateway:
    return VmsBootGatewayImpl()

@bind
def make_vms_snapshots_gateway() -> IVmsSnapshotsGateway:
    return VmsSnapshotsGateway()