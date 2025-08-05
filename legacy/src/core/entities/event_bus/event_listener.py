from abc import ABC, abstractmethod

from src.core.entities.event_bus import Event


class EventListener[E: Event](ABC):
    @abstractmethod
    def on_attach(self) -> None: pass

    @abstractmethod
    def on_detach(self) -> None: pass

    @abstractmethod
    def on_event(self, event: E) -> None: pass
