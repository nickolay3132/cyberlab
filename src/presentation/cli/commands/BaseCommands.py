from dataclasses import dataclass


from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCase, InstallUseCaseDTO
from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCase, ShutdownUseCaseDTO
from src.core.use_cases.vm_commands.StartupUseCase import StartupUseCase, StartupUseCaseDTO


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
        self.startup_use_case.execute(StartupUseCaseDTO())

    def shutdown(self, args):
        self.shutdown_use_case.execute(ShutdownUseCaseDTO(
            force=args.force,
        ))
