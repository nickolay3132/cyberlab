from abc import abstractmethod
from typing import Self

from src.core.entities.event_bus import EventBuilder
from src.core.entities.event_bus.events import StrEventTypes, StrEvent


class StrEventBuilder(EventBuilder):
    @abstractmethod
    def set_data(self, ev_data: str) -> Self: pass

    @abstractmethod
    def build(self) -> StrEvent: pass