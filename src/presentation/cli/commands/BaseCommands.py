from dataclasses import dataclass

from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCase, InstallUseCaseDTO
from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCase, ShutdownUseCaseDTO
from src.core.use_cases.vm_commands.StartupUseCase import StartupUseCase, StartupUseCaseDTO
from src.presentation.cli.observers.progressbar_cli_observer import ProgressBarCLIObserver
from src.presentation.cli.observers.texts_cli_observer import TextsCLIObserver


@dataclass
class BaseCommands:
    install_use_case: InstallUseCase
    startup_use_case: StartupUseCase
    shutdown_use_case: ShutdownUseCase

    def install(self, args):
        texts_observer = TextsCLIObserver()
        progress_bar_observer = ProgressBarCLIObserver()
        self.install_use_case.subject.attach(texts_observer)
        self.install_use_case.subject.attach(progress_bar_observer)

        self.install_use_case.execute(InstallUseCaseDTO(
            skip_download=args.skip_download,
            no_verify=args.no_verify,
        ))

    def startup(self, args):
        texts_observer = TextsCLIObserver()
        self.startup_use_case.subject.attach(texts_observer)

        self.startup_use_case.execute(StartupUseCaseDTO())

    def shutdown(self, args):
        texts_observer = TextsCLIObserver()
        self.shutdown_use_case.subject.attach(texts_observer)

        self.shutdown_use_case.execute(ShutdownUseCaseDTO(
            force=args.force,
        ))