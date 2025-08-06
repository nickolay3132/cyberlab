from pprint import pprint
from typing import List

from src.core.entities.event_bus import IEvent, IEventBus, IEventListener


class EventBusImpl[E: IEvent](IEventBus[E]):
    def __init__(self):
        self.listeners: List[IEventListener[E]] = []

    def attach(self, event_listener: IEventListener[E]):
        self.listeners.append(event_listener)

    def detach(self, event_listener: IEventListener[E]):
        self.listeners.remove(event_listener)

    def notify(self, event: IEvent):
        pprint(event)
        for listener in self.listeners:
            listener.on_event(event)