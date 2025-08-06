from src.bootstrap import get
from src.bootstrap.binder import bind

from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import ProgressEvent, TextEvent
from src.core.use_cases import InstallUseCase, FetchConfigUseCase, StartupUseCase

from src.core.interfaces.repositories import IStorageRepository, IVMRepository

from src.core.interfaces.services import IFileSystemService
from src.core.interfaces.services.vms import IInstallVMService, IImportVMService, IVmNetworkService, IVmBootService
from src.core.use_cases.shutdown_use_case import ShutdownUseCase

from src.infrastructure.repositories import YamlLoader


@bind
def make_fetch_config_use_case(file_system_service: IFileSystemService) -> FetchConfigUseCase:
    return FetchConfigUseCase(file_system_service)

@bind
def make_install_use_case(config_path: str, snapshots_path: str) -> InstallUseCase:
    text_event_bus = get(IEventBus[TextEvent])()
    progress_event_bus = get(IEventBus[ProgressEvent])()

    yaml_loader = get(YamlLoader)(config_path)
    storage_repo = get(IStorageRepository)(yaml_loader)
    vms_repo = get(IVMRepository)(yaml_loader)

    install_vm_service = get(IInstallVMService)()
    import_vm_service = get(IImportVMService)()
    vm_networks_service = get(IVmNetworkService)()

    return InstallUseCase(
        text_ev_bus=text_event_bus,
        progress_ev_bus=progress_event_bus,
        storage_repo=storage_repo,
        vm_repo=vms_repo,
        install_vm_service=install_vm_service,
        import_vm_service=import_vm_service,
        vm_network_service=vm_networks_service
    )

@bind
def make_startup_use_case(config_path: str) -> StartupUseCase:
    yaml_loader = get(YamlLoader)(config_path)
    vms_repo = get(IVMRepository)(yaml_loader)

    text_event_bus = get(IEventBus[TextEvent])()

    vm_boot_service = get(IVmBootService)()

    return StartupUseCase(
        vms_repo=vms_repo,
        vm_boot_service=vm_boot_service,
        text_ev_bus=text_event_bus,
    )

@bind
def make_shutdown_use_case(config_path: str) -> ShutdownUseCase:
    yaml_loader = get(YamlLoader)(config_path)
    vms_repo = get(IVMRepository)(yaml_loader)

    text_event_bus = get(IEventBus[TextEvent])()

    vm_boot_service = get(IVmBootService)()

    return ShutdownUseCase(
        vms_repo=vms_repo,
        vm_boot_service=vm_boot_service,
        text_ev_bus=text_event_bus,
    )