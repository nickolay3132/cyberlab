from dependency_injector import containers, providers

from src.core.use_cases.vm_commands.InstallCommand import InstallCommand


class UseCases(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()

    install_command=providers.Factory(
        InstallCommand,
        virtual_machines_installer_service=services.virtual_machines_installer_service,
    )