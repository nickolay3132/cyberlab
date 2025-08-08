from abc import ABC, abstractmethod
from typing import Type, Callable, TypeVar

from src.core.entities.event_bus import IEvent


E = TypeVar('E', bound=IEvent)
ListenerCallback = Callable[[E], None]

class IEventBus(ABC):
    @abstractmethod
    def attach(self, event_type: Type[E], listener: ListenerCallback) -> None: pass

    @abstractmethod
    def detach(self, event_type: Type[E], listener: ListenerCallback) -> None: pass

    @abstractmethod
    def notify(self, event: IEvent): pass
