from dependency_injector import containers, providers

from src.presentation.commands.BaseCommands import BaseCommands


class Commands (containers.DeclarativeContainer):
    use_cases = providers.DependenciesContainer()

    base_commands = providers.Factory(
        BaseCommands,
        install_use_case = use_cases.install_use_case,
        startup_use_case = use_cases.startup_use_case,
        shutdown_use_case = use_cases.shutdown_use_case,
    )