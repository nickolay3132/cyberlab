from dependency_injector import containers, providers

from src.core.use_cases.snapshots.RestoreSnapshotUseCase import RestoreSnapshotUseCase
from src.core.use_cases.snapshots.ListSnapshotsUseCase import ListSnapshotsUseCase
from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCase
from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCase
from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCase
from src.core.use_cases.vm_commands.StartupUseCase import StartupUseCase


class UseCases(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    observers = providers.DependenciesContainer()

    install_use_case=providers.Factory(
        InstallUseCase,
        virtual_machines_installer_service=services.virtual_machines_installer_service,
        vboxmanage_service=services.vboxmanage_service,
        vbox_snapshots_service=services.vbox_snapshots_service,
        subject=observers.subject,
    )

    startup_use_case=providers.Factory(
        StartupUseCase,
        vboxmanage_service=services.vboxmanage_service,
        subject=observers.subject,
    )

    shutdown_use_case=providers.Factory(
        ShutdownUseCase,
        vboxmanage_service=services.vboxmanage_service,
        subject=observers.subject,
    )

    create_snapshot_use_case=providers.Factory(
        CreateSnapshotUseCase,
        vbox_snapshots_service=services.vbox_snapshots_service,
        subject=observers.subject,
    )

    list_snapshots_use_case=providers.Factory(
        ListSnapshotsUseCase,
        vbox_snapshots_service=services.vbox_snapshots_service,
        subject=observers.subject,
    )

    restore_snapshot_use_case=providers.Factory(
        RestoreSnapshotUseCase,
        vbox_snapshots_service=services.vbox_snapshots_service,
        subject=observers.subject,
    )