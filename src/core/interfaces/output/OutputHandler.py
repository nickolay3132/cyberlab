from abc import ABC, abstractmethod

from src.core.interfaces.output.ProgressBar import ProgressBar


class OutputHandler (ABC):
    @abstractmethod
    def show_error(self, message) -> None: pass

    @abstractmethod
    def show_warning(self, message) -> None: pass

    @abstractmethod
    def show(self, text: str) -> None: pass

    @abstractmethod
    def space(self) -> None: pass

    @abstractmethod
    def new_progress_bar(self) -> ProgressBar: pass

    @abstractmethod
    def progress_bar(self) -> ProgressBar: pass