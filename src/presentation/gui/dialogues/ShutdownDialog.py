from typing import Dict

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QLabel

from src.infrastructure.containers.UseCases import UseCases
from src.presentation.gui.dialogues.Dialog import Dialog
from src.presentation.gui.gui_observer import GUIObserver
from src.presentation.gui.widgets.statuses_panel import StatusesPanel


class ShutdownDialog(Dialog):
    shutdown_force: QtWidgets.QCheckBox

    def __init__(self, use_cases: UseCases, observer: GUIObserver, parent=None):
        super().__init__(use_cases, observer, parent)
        self.setWindowTitle("Shutdown Parameters")

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.shutdown_force = QtWidgets.QCheckBox("Shutdown force")
        layout.addWidget(self.shutdown_force)
        layout.addLayout(self.buttons_layout())

    def execute(self):
        if self.shutdown_force.isChecked():
            pass
        self.accept()
