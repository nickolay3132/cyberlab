from dependency_injector import containers, providers

from src.infrastructure.cli.OutputHandlerImpl import OutputHandlerImpl


class Output(containers.DeclarativeContainer):

    cli_output_handler=providers.Factory(
        OutputHandlerImpl
    )