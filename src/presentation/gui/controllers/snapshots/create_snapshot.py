import time
from pprint import pprint
from typing import Callable, Optional

from PyQt6.QtWidgets import QWidget

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, SnapshotsTreeEvent
from src.core.use_cases.snapshots import CreateSnapshotUseCase, CreateSnapshotUseCaseDto, ListSnapshotsUseCase, \
    ListSnapshotsUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.modals import SnapshotCreationModal


def create_snapshot_controller(text_listener: Callable[[TextEvent], None],
                               snapshots_tree_listener: Callable[[SnapshotsTreeEvent], None],):
    create_snapshot_use_case = get(CreateSnapshotUseCase, f"{global_vars['root_dir']}/config.yaml", f"{global_vars['root_dir']}/snapshots.yaml")
    create_snapshot_use_case.ev_bus.attach(TextEvent, text_listener)

    def rerender_tree():
        time.sleep(2)
        list_snapshots_use_case = get(ListSnapshotsUseCase, f"{global_vars['root_dir']}/snapshots.yaml")
        list_snapshots_use_case.ev_bus.attach(SnapshotsTreeEvent, snapshots_tree_listener)
        list_snapshots_use_case_dto = ListSnapshotsUseCaseDto()
        run_usecase_async(list_snapshots_use_case, list_snapshots_use_case_dto, lambda: None)

    def on_submit(name: str, description: str = ''):
        create_snapshot_use_case_dto = CreateSnapshotUseCaseDto(name, description)

        run_usecase_async(create_snapshot_use_case, create_snapshot_use_case_dto, rerender_tree)

    SnapshotCreationModal(on_submit).exec()