from dependency_injector import containers, providers

from src.core.use_cases.cyber_lab_info_use_case import CyberLabInfoUseCase
from src.core.use_cases.snapshots.RestoreSnapshotUseCase import RestoreSnapshotUseCase
from src.core.use_cases.snapshots.ListSnapshotsUseCase import ListSnapshotsUseCase
from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCase
from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCase
from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCase
from src.core.use_cases.vm_commands.StartupUseCase import StartupUseCase


class UseCases(containers.DeclarativeContainer):
    presentation_config = providers.Configuration()
    repositories = providers.DependenciesContainer()
    services = providers.DependenciesContainer()
    event_buses = providers.DependenciesContainer()

    is_cli_mode = providers.Callable(
        lambda  config: config['mode'] == 'cli',
        presentation_config,
    )

    cyberlab_info_use_case = providers.Singleton(
        CyberLabInfoUseCase,
        no_display=is_cli_mode,
        vms_repository=repositories.virtual_machines_repository,
        info_event_bus=event_buses.vms_info_event_bus,
        cyber_lab_info_service=services.cyber_lab_info_service
    )

    install_use_case=providers.Factory(
        InstallUseCase,
        virtual_machines_installer_service=services.virtual_machines_installer_service,
        vboxmanage_service=services.vboxmanage_service,
        vbox_snapshots_service=services.vbox_snapshots_service,
        str_event_bus=event_buses.str_event_bus,
        # vms_info_event_bus=event_buses.vms_info_event_bus,
        info_use_case=cyberlab_info_use_case,
    )

    startup_use_case=providers.Factory(
        StartupUseCase,
        vboxmanage_service=services.vboxmanage_service,
        info_use_case=cyberlab_info_use_case,
    )

    shutdown_use_case=providers.Factory(
        ShutdownUseCase,
        vboxmanage_service=services.vboxmanage_service,
        info_use_case=cyberlab_info_use_case,
    )

    create_snapshot_use_case=providers.Factory(
        CreateSnapshotUseCase,
        vbox_snapshots_service=services.vbox_snapshots_service,
        info_use_case=cyberlab_info_use_case,
    )

    list_snapshots_use_case=providers.Factory(
        ListSnapshotsUseCase,
        vbox_snapshots_service=services.vbox_snapshots_service,
    )

    restore_snapshot_use_case=providers.Factory(
        RestoreSnapshotUseCase,
        vbox_snapshots_service=services.vbox_snapshots_service,
    )