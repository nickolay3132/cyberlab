import time
from typing import Callable

from PyQt6.QtWidgets import QStackedWidget, QWidget

from src.presentation.gui.ui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


class MainController:
    def __init__(self, set_central_widget: Callable[[QWidget], None]):
        self.set_central_widget = set_central_widget

    def show_main_page(self):
        page = VmsStatusesPage()

        def execute():
            print("Usecase running...")
            time.sleep(5)

        def on_complete():
            print("Usecase complete")

        # self.stack.addWidget(page)
        # self.stack.setCurrentWidget(page)
        self.set_central_widget(page)

        run_usecase_async(execute, on_complete)