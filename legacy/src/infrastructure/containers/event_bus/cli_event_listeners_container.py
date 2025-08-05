from dependency_injector import containers, providers

from src.presentation.cli.event_listeners import ProgressEventListener, SelectOptionEventListener, \
    SnapshotsTreeEventListener, StrEventListener


class CliEventListenerContainer(containers.DeclarativeContainer):
    progress_event_listener = providers.Singleton(ProgressEventListener)
    select_option_event_listener = providers.Singleton(SelectOptionEventListener)
    snapshots_tree_event_listener = providers.Singleton(SnapshotsTreeEventListener)
    str_event_listener = providers.Singleton(StrEventListener)
    vms_info_event_listener = providers.Singleton(StrEventListener)