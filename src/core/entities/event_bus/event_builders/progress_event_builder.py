from abc import ABC, abstractmethod
from typing import Self

from src.core.entities.event_bus import EventBuilder
from src.core.entities.event_bus.events import ProgressEventTypes, ProgressEvent


class ProgressEventBuilder(EventBuilder):
    @abstractmethod
    def set_type(self, ev_type: ProgressEventTypes) -> Self: pass

    @abstractmethod
    def build(self) -> ProgressEvent: pass