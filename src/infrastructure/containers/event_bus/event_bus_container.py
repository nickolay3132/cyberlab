from dependency_injector import containers, providers

from src.core.entities.event_bus import EventListener
from src.infrastructure.event_bus import EventBusImpl

def build_event_bus(event_listener: EventListener):
    event_bus_impl = EventBusImpl()
    event_bus_impl.attach(event_listener)
    return event_bus_impl


class EventBusContainer(containers.DeclarativeContainer):
    event_listeners = providers.DependenciesContainer()

    str_event_bus = providers.Singleton(
        build_event_bus,
        event_listener=event_listeners.str_event_listener
    )

    progress_event_bus = providers.Singleton(
        build_event_bus,
        event_listener=event_listeners.progress_event_listener
    )

    snapshots_tree_event_bus = providers.Singleton(
        build_event_bus,
        event_listener=event_listeners.snapshots_tree_event_listener
    )

    select_option_event_bus = providers.Singleton(
        build_event_bus,
        event_listener=event_listeners.select_option_event_listener
    )


