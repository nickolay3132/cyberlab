from typing import Callable

from PyQt6.QtWidgets import QWidget

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.core.use_cases import ShutdownUseCase, ShutdownUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


def shutdown_controller(set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
    page = VmsStatusesPage()
    set_central_widget(page)

    use_case = get(ShutdownUseCase, f"{global_vars['root_dir']}/config.yaml")
    use_case.ev_bus.attach(VmsListEvent, page.vms_list_event_listener)
    use_case.ev_bus.attach(TextEvent, page.text_event_listener)

    dto = ShutdownUseCaseDto(False)
    run_usecase_async(use_case, dto, on_complete)
