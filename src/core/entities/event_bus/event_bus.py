from abc import ABC, abstractmethod
from typing import Type, Callable

from src.core.entities.event_bus import IEvent


class IEventBus(ABC):
    @abstractmethod
    def attach(self, event_type: Type[IEvent], listener: Callable[[IEvent], None]): pass

    @abstractmethod
    def detach(self, event_type: Type[IEvent], listener: Callable[[IEvent], None]): pass

    @abstractmethod
    def notify(self, event: IEvent): pass
