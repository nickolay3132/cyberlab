from abc import ABC, abstractmethod


class ProgressBar (ABC):
    @abstractmethod
    def update(self, current: int, total: int) -> None: pass

    @abstractmethod
    def close(self) -> None: pass