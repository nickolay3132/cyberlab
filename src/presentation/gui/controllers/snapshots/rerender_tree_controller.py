import time
from typing import Callable

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import SnapshotsTreeEvent
from src.core.use_cases.snapshots import ListSnapshotsUseCase, ListSnapshotsUseCaseDto
from src.presentation.gui.controllers import run_usecase_async


def rerender_tree_controller(snapshots_tree_listener: Callable[[SnapshotsTreeEvent], None],):
    time.sleep(2)
    list_snapshots_use_case = get(ListSnapshotsUseCase, f"{global_vars['root_dir']}/snapshots.yaml")
    list_snapshots_use_case.ev_bus.attach(SnapshotsTreeEvent, snapshots_tree_listener)
    list_snapshots_use_case_dto = ListSnapshotsUseCaseDto()
    run_usecase_async(list_snapshots_use_case, list_snapshots_use_case_dto, lambda: None)