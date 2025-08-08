from typing import Callable

from PyQt6.QtWidgets import QWidget

import src
from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.core.use_cases import InstallUseCase, InstallUseCaseDto
from src.presentation.gui.ui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


class InstallController:
    def __init__(self, set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
        self.set_central_widget = set_central_widget
        self.on_complete = on_complete

    def run(self):
        page = VmsStatusesPage()
        self.set_central_widget(page)

        use_case = get(InstallUseCase)(f"{global_vars['root_dir']}/config.yaml", "")
        use_case.ev_bus.attach(VmsListEvent, page.vms_list_event_listener)
        use_case.ev_bus.attach(TextEvent, page.text_event_listener)

        dto = InstallUseCaseDto(src.__repository__, False, False)
        run_usecase_async(use_case, dto, self.on_complete)