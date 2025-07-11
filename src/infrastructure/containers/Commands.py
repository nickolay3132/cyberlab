from dependency_injector import containers, providers

from src.presentation.cli.commands.BaseCommands import BaseCommands
from src.presentation.cli.commands.SnapshotCommands import SnapshotCommands


class Commands (containers.DeclarativeContainer):
    use_cases = providers.DependenciesContainer()

    base_commands = providers.Factory(
        BaseCommands,
        install_use_case = use_cases.install_use_case,
        startup_use_case = use_cases.startup_use_case,
        shutdown_use_case = use_cases.shutdown_use_case,
    )

    snapshot_commands = providers.Factory(
        SnapshotCommands,
        create_snapshot_use_case = use_cases.create_snapshot_use_case,
    )