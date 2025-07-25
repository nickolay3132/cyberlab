from dependency_injector import containers, providers

from src.infrastructure.services.FileSystemServiceImpl import FileSystemServiceImpl
from src.infrastructure.services.ParallelTasksServiceImpl import ParallelTasksServiceImpl
from src.infrastructure.services.snapshots.SnapshotsTreeServiceImpl import SnapshotsTreeServiceImpl
from src.infrastructure.services.snapshots.VBoxSnapshotsServiceImpl import VBoxSnapshotsServiceImpl
from src.infrastructure.services.vbox.VBoxBootServiceImpl import VBoxBootServiceImpl
from src.infrastructure.services.vbox.VBoxImportServiceImpl import VBoxImportServiceImpl
from src.infrastructure.services.vbox.VBoxManageServiceImpl import VBoxManageServiceImpl
from src.infrastructure.services.vbox.VBoxNetworksImpl import VBoxNetworksImpl
from src.infrastructure.services.VIrtualMachinesInstallerServiceImpl import VirtualMachinesInstallerServiceImpl


class Services (containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()
    output = providers.DependenciesContainer()

    file_system_service = providers.Factory(
        FileSystemServiceImpl,
    )

    vbox_networks_service = providers.Factory(
        VBoxNetworksImpl,
        virtual_machines_repository=repos.virtual_machines_repository,
    )

    parallel_tasks_service = providers.Factory(
        ParallelTasksServiceImpl,
    )

    vbox_import_service = providers.Factory(
        VBoxImportServiceImpl,
        parallel_tasks_service=parallel_tasks_service,
        file_system_service=file_system_service,

        storage_repository=repos.storage_repository,
        virtual_machines_repository=repos.virtual_machines_repository,
    )

    vbox_boot_service = providers.Factory(
        VBoxBootServiceImpl,
        virtual_machines_repository=repos.virtual_machines_repository,
    )

    virtual_machines_installer_service = providers.Factory(
        VirtualMachinesInstallerServiceImpl,
        storage_repository=repos.storage_repository,
        virtual_machines_repository=repos.virtual_machines_repository,
        file_system_service=file_system_service,
    )

    vboxmanage_service = providers.Factory(
        VBoxManageServiceImpl,
        vbox_networks_service=vbox_networks_service,
        vbox_import_service=vbox_import_service,
        vbox_boot_service=vbox_boot_service,
    )

    vbox_snapshots_service = providers.Factory(
        VBoxSnapshotsServiceImpl,
        virtual_machines_repository=repos.virtual_machines_repository,
        snapshots_repository=repos.snapshots_repository,
    )