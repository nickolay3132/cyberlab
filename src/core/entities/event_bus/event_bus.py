from abc import abstractmethod, ABC
from typing import Self

from src.core.entities.event_bus import Event, EventListener


class EventBus[L: EventListener, E: Event](ABC):
    @abstractmethod
    def attach(self, listener: L) -> Self: pass

    @abstractmethod
    def detach(self, listener: L) -> Self: pass

    @abstractmethod
    def notify(self, event: E) -> Self: pass