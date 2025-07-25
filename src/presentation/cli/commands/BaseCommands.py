import threading
from dataclasses import dataclass
from typing import cast

from tqdm import tqdm

from src.core.entities.observer import Observer, ObserverEvent
from src.core.entities.progress_bar_data import ProgressBarData, ProgressBarStates
from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCase, InstallUseCaseDTO
from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCase, ShutdownUseCaseDTO
from src.core.use_cases.vm_commands.StartupUseCase import StartupUseCase, StartupUseCaseDTO


@dataclass
class BaseCommands:
    install_use_case: InstallUseCase
    startup_use_case: StartupUseCase
    shutdown_use_case: ShutdownUseCase

    def install(self, args):
        # TODO: example of multithreading startup, remove after creating gui
        observer = InstallObserver()
        self.install_use_case.subject.attach(observer)
        dto = InstallUseCaseDTO(
            skip_download=args.skip_download,
            no_verify=args.no_verify,
        )
        def runner():
            self.install_use_case.execute(dto)
        thread = threading.Thread(target=runner)
        thread.start()


    def startup(self, args):
        self.startup_use_case.subject.attach(InstallObserver())
        self.startup_use_case.execute(StartupUseCaseDTO())

    def shutdown(self, args):
        self.shutdown_use_case.subject.attach(InstallObserver())
        self.shutdown_use_case.execute(ShutdownUseCaseDTO(
            force=args.force,
        ))


class InstallObserver(Observer):
    def __init__(self):
        self.pbar = None

    def update(self, data: ObserverEvent) -> None:
        item_id = data.id
        ev_type = data.type
        data = data.data

        if ev_type == "space":
            print()

        if ev_type == "title":
            print(f"Title: {data}")

        if ev_type == "error":
            print(f"Error: {data}")

        if ev_type == "warning":
            print(f"Warning: {data}")

        if ev_type == "text":
            print(data)

        if ev_type == "success":
            print(f"Success: {data}")

        if ev_type == "progress":
            pb_data = cast(ProgressBarData, data)
            match pb_data.state:
                case ProgressBarStates.INIT:
                    print(f'Downloading {item_id}...')
                    self.pbar = tqdm(total=pb_data.total, unit="B", unit_scale=True)
                case ProgressBarStates.IN_PROGRESS:
                    self.pbar.update(pb_data.actual - self.pbar.n)
                case ProgressBarStates.COMPLETED:
                    self.pbar.close()
                case ProgressBarStates.ERROR:
                    self.pbar.close()
                    print(f"Error: {pb_data.error_msg}")