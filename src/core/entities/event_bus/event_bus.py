from abc import ABC, abstractmethod

from src.core.entities.event_bus import IEventListener, IEvent


class IEventBus[E: IEvent](ABC):
    @abstractmethod
    def attach(self, event_listener: IEventListener[E]): pass

    @abstractmethod
    def detach(self, event_listener: IEventListener[E]): pass

    @abstractmethod
    def notify(self, event: IEvent): pass
