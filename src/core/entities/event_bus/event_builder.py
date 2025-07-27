from abc import ABC, abstractmethod
from typing import Self


class EventBuilder(ABC):
    @abstractmethod
    def set_id(self, ev_id: str) -> Self: pass