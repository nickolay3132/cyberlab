from src.bootstrap import get
from src.bootstrap.binder import bind

from src.core.entities.event_bus import IEventBus
from src.core.interfaces.gateways import IVMsGateway
from src.core.use_cases import InstallUseCase, StartupUseCase, CyberLabStateUseCase

from src.core.interfaces.repositories import IStorageRepository, IVMRepository, ISnapshotsRepository

from src.core.interfaces.services import IFileSystemService
from src.core.interfaces.services.vms import IInstallVMService, IImportVMService, IVmNetworkService, IVmBootService, \
    IVmSnapshotsService
from src.core.use_cases.shutdown_use_case import ShutdownUseCase
from src.core.use_cases.snapshots import CreateSnapshotUseCase, ListSnapshotsUseCase, RestoreSnapshotUseCase

from src.infrastructure.repositories import YamlLoader


@bind
def make_cyber_lab_info_use_case(config_path: str) -> CyberLabStateUseCase:
    vm_gateway = get(IVMsGateway)
    ev_bus = get(IEventBus)

    yaml_loader = get(YamlLoader, config_path)
    vms_repo = get(IVMRepository, yaml_loader)
    storage_repo = get(IStorageRepository, yaml_loader)

    file_system_service = get(IFileSystemService)

    return CyberLabStateUseCase(
        vm_gateway=vm_gateway,
        ev_bus=ev_bus,
        vms_repo=vms_repo,
        storage_repo=storage_repo,
        filesystem_service=file_system_service,
    )

@bind
def make_install_use_case(config_path: str, snapshots_path: str) -> InstallUseCase:
    ev_bus = get(IEventBus)

    config_yaml_loader = get(YamlLoader, config_path)
    snapshots_yaml_loader = get(YamlLoader, snapshots_path)

    storage_repo = get(IStorageRepository, config_yaml_loader)
    vms_repo = get(IVMRepository, config_yaml_loader)
    snapshots_repo = get(ISnapshotsRepository, snapshots_yaml_loader)

    install_vm_service = get(IInstallVMService)
    import_vm_service = get(IImportVMService)
    vm_networks_service = get(IVmNetworkService)
    snapshot_service = get(IVmSnapshotsService)

    return InstallUseCase(
        ev_bus=ev_bus,
        storage_repo=storage_repo,
        vm_repo=vms_repo,
        snapshots_repo=snapshots_repo,
        install_vm_service=install_vm_service,
        import_vm_service=import_vm_service,
        vm_network_service=vm_networks_service,
        snapshots_service=snapshot_service,
    )

@bind
def make_startup_use_case(config_path: str) -> StartupUseCase:
    yaml_loader = get(YamlLoader, config_path)
    vms_repo = get(IVMRepository, yaml_loader)

    ev_bus = get(IEventBus)

    vm_boot_service = get(IVmBootService)

    return StartupUseCase(
        vms_repo=vms_repo,
        vm_boot_service=vm_boot_service,
        ev_bus=ev_bus,
    )

@bind
def make_shutdown_use_case(config_path: str) -> ShutdownUseCase:
    yaml_loader = get(YamlLoader, config_path)
    vms_repo = get(IVMRepository, yaml_loader)

    ev_bus = get(IEventBus)

    vm_boot_service = get(IVmBootService)

    return ShutdownUseCase(
        vms_repo=vms_repo,
        vm_boot_service=vm_boot_service,
        ev_bus=ev_bus,
    )

@bind
def make_create_snapshot_use_case(config_path: str, snapshots_path: str) -> CreateSnapshotUseCase:
    config_yaml_loader = get(YamlLoader, config_path)
    snapshots_yaml_loader = get(YamlLoader, snapshots_path)

    vms_repo = get(IVMRepository, config_yaml_loader)
    snapshots_repo = get(ISnapshotsRepository, snapshots_yaml_loader)

    ev_bus = get(IEventBus)

    vm_snapshots_service = get(IVmSnapshotsService)

    return CreateSnapshotUseCase(
        ev_bus=ev_bus,
        vms_repo=vms_repo,
        snapshots_repo=snapshots_repo,
        snapshots_service=vm_snapshots_service,
    )

@bind
def make_list_snapshots_use_case(snapshots_path: str) -> ListSnapshotsUseCase:
    snapshots_yaml_loader = get(YamlLoader, snapshots_path)
    snapshots_repo = get(ISnapshotsRepository, snapshots_yaml_loader)

    ev_bus = get(IEventBus)

    return ListSnapshotsUseCase(
        snapshots_repo=snapshots_repo,
        ev_bus=ev_bus,
    )

@bind
def make_restore_snapshot_use_case(config_path: str, snapshots_path: str) -> RestoreSnapshotUseCase:
    config_yaml_loader = get(YamlLoader, config_path)
    snapshots_yaml_loader = get(YamlLoader, snapshots_path)

    vms_repo = get(IVMRepository, config_yaml_loader)
    snapshots_repo = get(ISnapshotsRepository, snapshots_yaml_loader)

    ev_bus = get(IEventBus)

    vm_snapshots_service = get(IVmSnapshotsService)

    return RestoreSnapshotUseCase(
        ev_bus=ev_bus,
        vms_repo=vms_repo,
        snapshots_repo=snapshots_repo,
        snapshots_service=vm_snapshots_service,
    )
