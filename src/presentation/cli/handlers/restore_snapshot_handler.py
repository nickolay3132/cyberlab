from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, SelectSnapshotEvent
from src.core.use_cases.snapshots import RestoreSnapshotUseCase, RestoreSnapshotUseCaseDto
from src.presentation.cli.event_listeners import text_event_listener, select_snapshot_event_listener


def handle_snapshot_restore(args):
    use_case = get(RestoreSnapshotUseCase, f"{global_vars['root_dir']}/config.yaml",
                   f"{global_vars['root_dir']}/snapshots.yaml")
    use_case.ev_bus.attach(TextEvent, text_event_listener)
    use_case.ev_bus.attach(SelectSnapshotEvent, select_snapshot_event_listener)

    dto = RestoreSnapshotUseCaseDto(args.name)
    use_case.execute(dto)