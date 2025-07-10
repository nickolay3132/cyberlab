from dependency_injector import containers, providers

from src.core.use_cases.vm_commands.InstallCommand import InstallCommand
from src.core.use_cases.vm_commands.ShutdownCommand import ShutdownCommand
from src.core.use_cases.vm_commands.StartupCommand import StartupCommand


class UseCases(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    output = providers.DependenciesContainer()

    install_command=providers.Factory(
        InstallCommand,
        virtual_machines_installer_service=services.virtual_machines_installer_service,
        vboxmanage_service=services.vboxmanage_service,
        output_handler=output.cli_output_handler,
    )

    startup_command=providers.Factory(
        StartupCommand,
        vboxmanage_service=services.vboxmanage_service,
    )

    shutdown_command=providers.Factory(
        ShutdownCommand,
        vboxmanage_service=services.vboxmanage_service,
    )