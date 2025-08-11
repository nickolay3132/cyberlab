import functools
from pprint import pprint
from typing import Callable

from PyQt6.QtWidgets import QWidget

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import SnapshotsTreeEvent, TextEvent
from src.core.enums.events import TextEventType
from src.core.use_cases.snapshots import ListSnapshotsUseCase, ListSnapshotsUseCaseDto, CreateSnapshotUseCase, \
    CreateSnapshotUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
# from src.presentation.gui.controllers.snapshots import create_snapshot_controller
from src.presentation.gui.ui.pages import SnapshotsPage

def _create_snapshot(name: str, description: str = '') -> None:
    from src.presentation.gui.controllers.snapshots import create_snapshot_controller

def list_snapshots_controller(set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
    from src.presentation.gui.controllers.snapshots import create_snapshot_controller

    page = SnapshotsPage()
    page.add_create_button(functools.partial(create_snapshot_controller, page.text_event_listener, page.snapshots_tree_listener))
    page.add_rollback_button(lambda snapshot: pprint(snapshot))
    page.add_back_home_button(lambda: print('back home'))

    set_central_widget(page)

    use_case = get(ListSnapshotsUseCase,f"{global_vars['root_dir']}/snapshots.yaml")
    use_case.ev_bus.attach(SnapshotsTreeEvent, page.snapshots_tree_listener)

    run_usecase_async(use_case, ListSnapshotsUseCaseDto(), on_complete)