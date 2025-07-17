from PyQt6 import QtWidgets

from src.presentation.gui.dialogues.Dialog import Dialog


class StartupDialog(Dialog):
    def __init__(self, cmd, command_executor, parent=None):
        super().__init__(cmd, command_executor, parent)
        self.setWindowTitle("Startup Parameters")
        self.cmd.extend(['startup'])

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(self.buttons_layout())

    def execute(self):
        self.command_executor.exec(self.cmd)
        self.accept()

