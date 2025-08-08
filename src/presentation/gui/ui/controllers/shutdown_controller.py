from typing import Callable

from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent
from src.core.use_cases import ShutdownUseCase, ShutdownUseCaseDto
from src.presentation.gui.ui.controllers import run_usecase_async, MainController
from src.presentation.gui.ui.pages import VmsStatusesPage


class ShutdownController:
    def __init__(self, set_central_widget: Callable[[QWidget], None]):
        self.set_central_widget = set_central_widget

    def show_shutdown_page(self):
        page = VmsStatusesPage()

        def execute():
            use_case = get(ShutdownUseCase)(f"{global_vars['root_dir']}/config.yaml")
            ev_bus = use_case.ev_bus

            ev_bus.attach(TextEvent, page.text_event_listener)

            dto = ShutdownUseCaseDto(False)
            use_case.execute(dto)

        def on_complete():
            print("shutdown complete")

        # self.stack.addWidget(page)
        # self.stack.setCurrentWidget(page)
        self.set_central_widget(page)

        run_usecase_async(execute, on_complete)