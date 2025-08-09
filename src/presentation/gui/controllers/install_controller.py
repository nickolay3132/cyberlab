from typing import Callable

from PyQt6.QtWidgets import QWidget

import src
from src.core.entities.event_bus.events import ProgressEvent
from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.core.use_cases import InstallUseCase, InstallUseCaseDto
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


def install_controller(set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
    page = VmsStatusesPage()
    set_central_widget(page)

    use_case = get(InstallUseCase, f"{global_vars['root_dir']}/config.yaml", "")
    use_case.ev_bus.attach(VmsListEvent, page.vms_list_event_listener)
    use_case.ev_bus.attach(TextEvent, page.text_event_listener)
    use_case.ev_bus.attach(ProgressEvent, page.progress_bar_event_listener)

    dto = InstallUseCaseDto(src.__repository__, False, False)
    run_usecase_async(use_case, dto, on_complete)