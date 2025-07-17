from dependency_injector import containers, providers

from src.infrastructure.cli.CLIInputHandlerImpl import CLIInputHandlerImpl
from src.infrastructure.cli.OutputHandlerImpl import OutputHandlerImpl


class CLIOutput(containers.DeclarativeContainer):

    cli_output_handler=providers.Factory(
        OutputHandlerImpl
    )

    input_handler=providers.Factory(
        CLIInputHandlerImpl
    )