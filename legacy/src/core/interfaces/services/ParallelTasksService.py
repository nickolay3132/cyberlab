from abc import ABC, abstractmethod
from typing import Callable, Tuple, List, Dict

from src.core.entities.ParrallelTask import ParallelTaskData


class ParallelTasksService(ABC):
    @abstractmethod
    def add_task(self, task: Callable, args: Dict) -> None: pass

    @abstractmethod
    def run(self) -> None: pass

    @abstractmethod
    def wait(self, on_complete: Callable[[ParallelTaskData], None]) -> None: pass