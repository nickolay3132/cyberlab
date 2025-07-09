from dependency_injector import containers, providers

from src.infrastructure.services.FileSystemServiceImpl import FileSystemServiceImpl
from src.infrastructure.services.ParallelTasksServiceImpl import ParallelTasksServiceImpl
from src.infrastructure.services.VBoxManageServiceImpl import VBoxManageServiceImpl
from src.infrastructure.services.VBoxNetworksImpl import VBoxNetworksImpl
from src.infrastructure.services.VIrtualMachinesInstallerServiceImpl import VirtualMachinesInstallerServiceImpl


class Services (containers.DeclarativeContainer):
    repos = providers.DependenciesContainer()
    output = providers.DependenciesContainer()

    file_system_service = providers.Factory(
        FileSystemServiceImpl,
    )

    vbox_networks_service = providers.Factory(
        VBoxNetworksImpl
    )

    parallel_tasks_service = providers.Factory(
        ParallelTasksServiceImpl,
    )

    virtual_machines_installer_service = providers.Factory(
        VirtualMachinesInstallerServiceImpl,
        storage_repository=repos.storage_repository,
        virtual_machines_repository=repos.virtual_machines_repository,
        file_system_service=file_system_service,
        output_handler=output.cli_output_handler,
    )

    vboxmanage_service = providers.Factory(
        VBoxManageServiceImpl,
        storage_repository=repos.storage_repository,
        virtual_machines_repository=repos.virtual_machines_repository,
        file_system_service=file_system_service,
        vbox_networks_service=vbox_networks_service,
        parallel_tasks_service=parallel_tasks_service,
        output_handler=output.cli_output_handler,
    )