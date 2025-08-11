from typing import Callable

from src.core.entities import Snapshot
from src.core.use_cases.snapshots import RestoreSnapshotUseCase, RestoreSnapshotUseCaseDto
from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent
from src.presentation.gui.controllers import run_usecase_async


def restore_snapshot_controller(text_listener: Callable[[TextEvent], None],
                                rerender_tree: Callable[[], None],
                                snapshot: Snapshot):
    use_case = get(RestoreSnapshotUseCase, f"{global_vars['root_dir']}/config.yaml",
                                    f"{global_vars['root_dir']}/snapshots.yaml")
    use_case.ev_bus.attach(TextEvent, text_listener)

    dto = RestoreSnapshotUseCaseDto(snapshot.name, snapshot.timestamp)
    run_usecase_async(use_case, dto, rerender_tree)





