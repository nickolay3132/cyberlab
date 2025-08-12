from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import SnapshotsTreeEvent
from src.core.use_cases.snapshots import ListSnapshotsUseCase, ListSnapshotsUseCaseDto
from src.presentation.cli.event_listeners import snapshots_tree_event_listener


def handle_snapshot_list(args):
    use_case = get(ListSnapshotsUseCase, f"{global_vars['root_dir']}/snapshots.yaml")
    use_case.ev_bus.attach(SnapshotsTreeEvent, snapshots_tree_event_listener)

    dto = ListSnapshotsUseCaseDto()
    use_case.execute(dto)