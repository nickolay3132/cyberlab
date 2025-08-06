from abc import ABC, abstractmethod
from typing import Callable, Dict

from src.core.entities import ParallelTask


class IParallelTaskService(ABC):
    @abstractmethod
    def add_task(self, task: Callable[[ParallelTask], None], args: Dict) -> None: pass

    @abstractmethod
    def run(self) -> None: pass

    @abstractmethod
    def wait(self, on_complete: Callable[[ParallelTask], None]) -> None: pass