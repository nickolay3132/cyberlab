from abc import abstractmethod
from asyncio import Future
from typing import List, Self

from src.core.entities.event_bus import EventBuilder
from src.core.entities.event_bus.events import SelectOptionEvent


class SelectOptionEventBuilder(EventBuilder):
    @abstractmethod
    def add_option(self, option: str) -> Self: pass

    @abstractmethod
    def set_options(self, options: List[str]) -> Self: pass

    @abstractmethod
    def set_future(self, future: Future) -> Self: pass

    @abstractmethod
    def build(self) -> SelectOptionEvent: pass
