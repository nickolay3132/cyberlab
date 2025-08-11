import functools
from typing import Callable

from PyQt6.QtWidgets import QWidget

import src
from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import SnapshotsTreeEvent
from src.core.use_cases.snapshots import ListSnapshotsUseCase, ListSnapshotsUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import SnapshotsPage


def list_snapshots_controller(set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
    page = SnapshotsPage()

    rerender_tree_controller = functools.partial(
        src.presentation.gui.controllers.snapshots.rerender_tree_controller,
        page.snapshots_tree_listener
    )

    create_snapshot_controller = functools.partial(
        src.presentation.gui.controllers.snapshots.create_snapshot_controller,
        page.text_event_listener,
        rerender_tree_controller
    )

    restore_controller = functools.partial(
        src.presentation.gui.controllers.snapshots.restore_snapshot_controller,
        page.text_event_listener,
        rerender_tree_controller,
    )

    back_home_controller = functools.partial(
        src.presentation.gui.controllers.main_controller,
        set_central_widget,
        on_complete
    )

    page.add_create_button(create_snapshot_controller)
    page.add_rollback_button(restore_controller)
    page.add_back_home_button(back_home_controller)

    set_central_widget(page)

    use_case = get(ListSnapshotsUseCase,f"{global_vars['root_dir']}/snapshots.yaml")
    use_case.ev_bus.attach(SnapshotsTreeEvent, page.snapshots_tree_listener)

    run_usecase_async(use_case, ListSnapshotsUseCaseDto(), on_complete)