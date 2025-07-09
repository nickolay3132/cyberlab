import sys

from colorama.ansi import Fore, Style

from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.output.ProgressBar import ProgressBar
from src.infrastructure.cli.ProgressBarImpl import ProgressBarImpl


class OutputHandlerImpl (OutputHandler):
    def __init__(self):
        self._pbar = None

    def show_error(self, message: str, terminate: bool = False) -> None:
        print(f"{Fore.RED}Error occurred! {message}{Style.RESET_ALL}")
        if terminate:
            sys.exit(1)

    def show_warning(self, message) -> None:
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def show(self, text: str) -> None:
        print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")

    def text(self, text: str) -> None:
        print(text)

    def success(self, text: str) -> None:
        print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

    def space(self) -> None:
        print()

    def new_progress_bar(self) -> None:
        self._pbar = ProgressBarImpl()

    def progress_bar(self) -> ProgressBar:
        if self._pbar is None:
            self.new_progress_bar()
        return self._pbar