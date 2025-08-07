from PyQt6.QtWidgets import QStackedWidget

from src.bootstrap import get, global_vars
from src.core.entities.event_bus import IEventBus
from src.core.entities.event_bus.events import TextEvent
from src.core.use_cases import ShutdownUseCase, ShutdownUseCaseDto
from src.presentation.gui.ui.controllers import run_usecase_async, MainController
from src.presentation.gui.ui.pages.shutdown_page import ShutdownPage


class ShutdownController:
    def __init__(self, stacked_widget: QStackedWidget):
        self.stack = stacked_widget

    def show_shutdown_page(self):
        page = ShutdownPage()

        def execute():
            ev_bus = get(IEventBus)()
            use_case = get(ShutdownUseCase)(f"{global_vars['root_dir']}/config.yaml")

            ev_bus.attach(TextEvent, page.text_event_listener)

            dto = ShutdownUseCaseDto(False)
            use_case.execute(dto)

        def on_complete():
            ev_bus = get(IEventBus)()
            ev_bus.detach(TextEvent, page.text_event_listener)

        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)

        run_usecase_async(execute, on_complete)