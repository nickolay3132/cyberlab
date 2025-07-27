from typing import Self, List, Optional, Type

from src.core.entities.event_bus import EventBus, EventListener, Event


class EventBusImpl[E: Event](EventBus):
    def __init__(self, listeners: Optional[List[Type[EventListener[E]]]] = None) -> None:
        self.listeners: List[Type[EventListener[E]]] = []

        if listeners:
            for listener in listeners:
                self.attach(listener)

    def attach(self, listener) -> Self:
        try:
            listener.on_attach()
        finally:
            self.listeners.append(listener)

    def detach(self, listener) -> Self:
        try:
            listener.on_detach()
        finally:
            self.listeners.remove(listener)

    def notify(self, event: E) -> Self:
        for listener in self.listeners:
            try:
                listener.on_event(event)
            finally:
                pass