from colorama.ansi import Fore

from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.output.ProgressBar import ProgressBar
from src.infrastructure.cli.ProgressBarImpl import ProgressBarImpl


class OutputHandlerImpl (OutputHandler):
    def __init__(self):
        self._pbar = None

    def show_error(self, message) -> None:
        print(f"{Fore.RED}Error occurred! Message: {message}")

    def new_progress_bar(self) -> None:
        self._pbar = ProgressBarImpl()

    def progress_bar(self) -> ProgressBar:
        if self._pbar is None:
            self.new_progress_bar()
        return self._pbar