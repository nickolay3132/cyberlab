from typing import List, Type, Callable, Dict, TypeVar

from src.core.entities.event_bus import IEvent, IEventBus


E = TypeVar('E', bound=IEvent)
ListenerCallback = Callable[[E], None]

class EventBusImpl(IEventBus):
    def __init__(self):
        #  Example: { TextEvent: [callback(event: TextEvent)] }
        self.listeners: Dict[Type[IEvent], List[ListenerCallback]] = {}

    def attach(self, event_type: Type[E], listener: ListenerCallback) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def detach(self, event_type: Type[E], listener: ListenerCallback) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type].remove(listener)

    def notify(self, event: IEvent):
        event_type = type(event)
        for listener in self.listeners.get(event_type, []):
            listener(event)