import time
from typing import Callable

from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.presentation.gui.ui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


class MainController:
    def __init__(self, set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
        self.set_central_widget = set_central_widget
        self.on_complete = on_complete

    def run(self):
        page = VmsStatusesPage()
        self.set_central_widget(page)
        self.on_complete()
        # def execute():
        #     print("Usecase running...")
        #     time.sleep(5)
        #
        # # self.stack.addWidget(page)
        # # self.stack.setCurrentWidget(page)
        # self.set_central_widget(page)
        #
        # run_usecase_async(execute, self.on_complete)