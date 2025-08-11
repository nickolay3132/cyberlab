from typing import Callable

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent
from src.core.use_cases.snapshots import CreateSnapshotUseCase, CreateSnapshotUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.modals import SnapshotCreationModal


def create_snapshot_controller(text_listener: Callable[[TextEvent], None],
                               rerender_tree: Callable[[], None],):
    use_case = get(CreateSnapshotUseCase, f"{global_vars['root_dir']}/config.yaml", f"{global_vars['root_dir']}/snapshots.yaml")
    use_case.ev_bus.attach(TextEvent, text_listener)

    def on_submit(name: str, description: str = ''):
        dto = CreateSnapshotUseCaseDto(name, description)

        run_usecase_async(use_case, dto, rerender_tree)

    SnapshotCreationModal(on_submit).exec()