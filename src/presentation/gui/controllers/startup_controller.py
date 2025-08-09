from typing import Callable

from PyQt6.QtWidgets import QWidget

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.core.use_cases import StartupUseCaseDto, StartupUseCase
from src.presentation.gui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


class StartupController:
    def __init__(self, set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
        self.set_central_widget = set_central_widget
        self.on_complete = on_complete

    def run(self):
        page = VmsStatusesPage()
        self.set_central_widget(page)

        use_case = get(StartupUseCase)(f"{global_vars['root_dir']}/config.yaml")
        use_case.ev_bus.attach(VmsListEvent, page.vms_list_event_listener)
        use_case.ev_bus.attach(TextEvent, page.text_event_listener)

        dto = StartupUseCaseDto()
        run_usecase_async(use_case, dto, self.on_complete)
