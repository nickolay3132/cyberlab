from dataclasses import dataclass

from src.core.use_cases.vm_commands.InstallCommand import InstallCommand, InstallCommandDTO
from src.core.use_cases.vm_commands.ShutdownCommand import ShutdownCommand, ShutdownCommandDTO
from src.core.use_cases.vm_commands.StartupCommand import StartupCommand, StartupCommandDTO


@dataclass
class BaseCommands:
    install_command: InstallCommand
    startup_command: StartupCommand
    shutdown_command: ShutdownCommand

    def install(self, args):
        install_use_case_dto = InstallCommandDTO(
            skip_download=args.skip_download,
            no_verify=args.no_verify,
        )

        self.install_command.execute(install_use_case_dto)

    def startup(self, args):
        startup_use_case_dto = StartupCommandDTO()

        self.startup_command.execute(startup_use_case_dto)

    def shutdown(self, args):
        shutdown_use_case_dto = ShutdownCommandDTO(
            force=args.force,
        )
        self.shutdown_command.execute(shutdown_use_case_dto)
