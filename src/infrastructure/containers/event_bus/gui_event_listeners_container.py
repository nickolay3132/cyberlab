from dependency_injector import containers, providers

from src.presentation.gui.event_listeners import StrEventListener, ProgressEventListener, SelectOptionEventListener, SnapshotsTreeEventListener


class GuiEventListenersContainer(containers.DeclarativeContainer):
    layout_map = providers.Configuration()

    progress_event_listener = providers.Factory(ProgressEventListener, layout_map=layout_map)
    select_option_event_listener = providers.Factory(SelectOptionEventListener)
    snapshots_tree_event_listener = providers.Factory(SnapshotsTreeEventListener)
    str_event_listener = providers.Factory(StrEventListener, layout_map=layout_map)
    vms_info_event_listener = providers.Factory(StrEventListener, layout_map=layout_map)