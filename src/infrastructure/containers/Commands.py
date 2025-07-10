from dependency_injector import containers, providers

from src.presentation.commands.BaseCommands import BaseCommands


class Commands (containers.DeclarativeContainer):
    use_cases = providers.DependenciesContainer()

    base_commands = providers.Factory(
        BaseCommands,
        install_command = use_cases.install_command,
        startup_command = use_cases.startup_command,
        shutdown_command = use_cases.shutdown_command,
    )