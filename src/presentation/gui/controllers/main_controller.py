from typing import Callable

from PyQt6.QtWidgets import QWidget

from src.presentation.gui.ui.pages import VmsStatusesPage


def main_controller(set_central_widget: Callable[[QWidget], None], on_complete: Callable[[], None]):
    page = VmsStatusesPage()
    set_central_widget(page)
    on_complete()