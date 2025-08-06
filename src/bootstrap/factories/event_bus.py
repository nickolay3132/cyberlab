from src.bootstrap.binder import bind
from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import ProgressEvent, TextEvent
from src.infrastructure.event_bus import EventBusImpl


@bind
def make_text_event_bus() -> IEventBus[TextEvent]:
    return EventBusImpl[TextEvent]()

@bind
def make_progress_event_bus() -> IEventBus[ProgressEvent]:
    return EventBusImpl[ProgressEvent]()