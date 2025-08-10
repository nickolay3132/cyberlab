from typing import List, Callable

from src.core.entities import Snapshot, VM
from src.core.interfaces.gateways import IVmsSnapshotsGateway
from src.core.interfaces.services.vms import IVmSnapshotsService


class VmSnapshotsServiceImpl(IVmSnapshotsService):
    def __init__(self, vms_snapshots_gateway: IVmsSnapshotsGateway):
        self.vms_snapshots_gateway = vms_snapshots_gateway

    def create_snapshot(self, vm: VM, snapshot: Snapshot) -> bool:
        return self.vms_snapshots_gateway.create_snapshot(vm, snapshot)

    def restore_snapshot(self, snapshot: Snapshot) -> bool:
        pass

    def select_snapshot(self, snapshots: List[Snapshot], callback: Callable[[int], None]) -> Snapshot:
        pass