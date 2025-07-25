from PyQt6 import QtWidgets

from src.infrastructure.containers.UseCases import UseCases
from src.presentation.gui.dialogues.Dialog import Dialog
from src.presentation.gui.gui_observer import GUIObserver


class StartupDialog(Dialog):
    def __init__(self, use_cases: UseCases, observer: GUIObserver, parent=None):
        super().__init__(use_cases, observer, parent)
        self.setWindowTitle("Startup Parameters")

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(self.buttons_layout())

    def execute(self):
        self.accept()

