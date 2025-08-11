from typing import Callable

from PyQt6.QtWidgets import QWidget

from src.bootstrap import global_vars, get
from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.core.use_cases import CyberLabStateUseCase, CyberLabStateUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


def main_controller(set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
    page = VmsStatusesPage()
    set_central_widget(page)

    use_case = get(CyberLabStateUseCase, f"{global_vars['root_dir']}/config.yaml")
    use_case.ev_bus.attach(VmsListEvent, page.vms_list_event_listener)
    use_case.ev_bus.attach(TextEvent, page.text_event_listener)

    dto = CyberLabStateUseCaseDto()
    run_usecase_async(use_case, dto, on_complete)
