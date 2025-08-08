from src.bootstrap.binder import bind
from src.core.entities.event_bus import IEventBus
from src.infrastructure.event_bus import EventBusImpl

ev_bus = EventBusImpl()

@bind
def make_event_bus() -> IEventBus:
    return EventBusImpl()