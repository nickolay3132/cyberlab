from typing import List, Type, Callable, Dict

from src.core.entities.event_bus import IEvent, IEventBus


class EventBusImpl(IEventBus):
    def __init__(self):
        self.listeners: Dict[IEvent, List[Callable[[IEvent], None]]] = {}

    def attach(self, event_type: IEvent, listener: Callable[[IEvent], None]) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def detach(self, event_type: IEvent, listener: Callable[[IEvent], None]) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type].remove(listener)

    def notify(self, event: IEvent):
        event_type = type(event)
        for listener in self.listeners.get(event_type, []):
            listener(event)