from dataclasses import dataclass


from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCase, InstallUseCaseDTO
from src.core.use_cases.vm_commands.ShutdownCommand import ShutdownCommand, ShutdownCommandDTO

from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCase
from src.core.use_cases.vm_commands.StartupUseCase import StartupCommand, StartupCommandDTO, StartupUseCase


@dataclass
class BaseCommands:
    install_use_case: InstallUseCase
    startup_use_case: StartupUseCase
    shutdown_use_case: ShutdownUseCase

    def install(self, args):
        self.install_use_case.execute(InstallUseCaseDTO(
            skip_download=args.skip_download,
            no_verify=args.no_verify,
        ))

    def startup(self, args):
        self.startup_use_case.execute(StartupCommandDTO())

    def shutdown(self, args):
        self.startup_use_case.execute(ShutdownCommandDTO(
            force=args.force,
        ))
