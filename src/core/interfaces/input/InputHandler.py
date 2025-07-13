from abc import ABC, abstractmethod
from typing import List, Callable


class InputHandler(ABC):
    @abstractmethod
    def select_option(self, data: List[str], callback: Callable[[int], None]) -> None: pass