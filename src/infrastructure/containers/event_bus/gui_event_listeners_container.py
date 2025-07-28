from dependency_injector import containers, providers

from src.presentation.gui.event_listeners import StrEventListener, ProgressEventListener, SelectOptionEventListener, SnapshotsTreeEventListener


class GuiEventListenersContainer(containers.DeclarativeContainer):
    layout_map = providers.Configuration()

    progress_event_listener = providers.Singleton(ProgressEventListener, layout_map=layout_map)
    select_option_event_listener = providers.Singleton(SelectOptionEventListener)
    snapshots_tree_event_listener = providers.Singleton(SnapshotsTreeEventListener)
    str_event_listener = providers.Singleton(StrEventListener, layout_map=layout_map)