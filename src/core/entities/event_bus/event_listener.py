from abc import ABC, abstractmethod

from src.core.entities.event_bus import IEvent


class IEventListener[E: IEvent](ABC):
    @abstractmethod
    def on_event(self, event: E) -> None: pass