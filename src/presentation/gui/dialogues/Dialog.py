from typing import List, Type

from PyQt6 import QtWidgets

from src.infrastructure.containers.UseCases import UseCases
from src.presentation.gui.observers.gui_observer_invoker import GUIObserverInvoker


class Dialog(QtWidgets.QDialog):
    execute_button: QtWidgets.QPushButton
    cancel_button: QtWidgets.QPushButton

    def __init__(self, use_cases: UseCases, observers: List[GUIObserverInvoker],  parent=None):
        super().__init__(parent)
        self.setModal(True)

        self.use_cases = use_cases
        self.observers = observers

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