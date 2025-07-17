from typing import List

from PyQt6 import QtWidgets

from src.presentation.gui.RunTerminalCommand import RunTerminalCommand


class Dialog(QtWidgets.QDialog):
    execute_button: QtWidgets.QPushButton
    cancel_button: QtWidgets.QPushButton

    def __init__(self, cmd: List[str], command_executor: RunTerminalCommand, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.cmd = cmd
        self.command_executor = command_executor
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