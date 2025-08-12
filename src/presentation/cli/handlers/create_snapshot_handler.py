from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent
from src.core.use_cases.snapshots import CreateSnapshotUseCase, CreateSnapshotUseCaseDto
from src.presentation.cli.event_listeners import text_event_listener


def handle_snapshot_create(args):
    config = f"{global_vars['root_dir']}/config.yaml"
    snapshots = f"{global_vars['root_dir']}/snapshots.yaml"

    use_case = get(CreateSnapshotUseCase, config, snapshots)
    use_case.ev_bus.attach(TextEvent, text_event_listener)

    dto = CreateSnapshotUseCaseDto(args.name, args.description)
    use_case.execute(dto)