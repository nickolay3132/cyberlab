from typing import List, Dict

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QLabel

from src.infrastructure.containers.UseCases import UseCases
from src.presentation.gui.RunTerminalCommand import RunTerminalCommand
from src.presentation.gui.gui_observer import GUIObserver


class Dialog(QtWidgets.QDialog):
    execute_button: QtWidgets.QPushButton
    cancel_button: QtWidgets.QPushButton

    def __init__(self, use_cases: UseCases, observer: GUIObserver,  parent=None):
        super().__init__(parent)
        self.setModal(True)

        self.use_cases = use_cases
        self.observer = observer

        self.setup_ui()

    def buttons_layout(self) -> QtWidgets.QHBoxLayout:
        button_layout = QtWidgets.QHBoxLayout()

        self.execute_button = QtWidgets.QPushButton("Execute")
        self.execute_button.clicked.connect(self.execute)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.execute_button)
        button_layout.addWidget(self.cancel_button)

        return button_layout

    def setup_ui(self):
        raise NotImplementedError(f"Method 'setup_ui' must be implemented in subclass {self.__class__.__name__}")

    def execute(self):
        raise NotImplementedError(f"Method 'execute' must be implemented in subclass {self.__class__.__name__}")