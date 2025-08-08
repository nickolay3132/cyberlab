import time

from PyQt6.QtWidgets import QStackedWidget

from src.presentation.gui.ui.controllers import run_usecase_async
from src.presentation.gui.ui.pages import VmsStatusesPage


class MainController:
    def __init__(self, stacked_widget: QStackedWidget):
        self.stack = stacked_widget

    def show_main_page(self):
        page = VmsStatusesPage()

        def execute():
            print("Usecase running...")  # ← безопасно
            time.sleep(5)  # ← имитация работы

        def on_complete():
            print("Usecase complete")

        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)

        run_usecase_async(execute, on_complete)