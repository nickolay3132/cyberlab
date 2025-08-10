from abc import abstractmethod, ABC
from typing import Self

from src.core.entities.event_bus import IEvent


class EventBus[E: IEvent](ABC):
    @abstractmethod
    def attach(self, listener) -> Self: pass

    @abstractmethod
    def detach(self, listener) -> Self: pass

    @abstractmethod
    def notify(self, event: E) -> Self: pass