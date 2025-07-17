from PyQt6 import QtWidgets

from src.presentation.gui.dialogues.Dialog import Dialog


class ShutdownDialog(Dialog):
    shutdown_force: QtWidgets.QCheckBox

    def __init__(self, cmd, command_executor, parent=None):
        super().__init__(cmd, command_executor, parent)
        self.setWindowTitle("Shutdown Parameters")
        self.cmd.extend(['shutdown'])

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.shutdown_force = QtWidgets.QCheckBox("Shutdown force")
        layout.addWidget(self.shutdown_force)
        layout.addLayout(self.buttons_layout())

    def execute(self):
        if self.shutdown_force.isChecked():
            self.cmd.extend(['--force'])

        self.command_executor.exec(self.cmd)
        self.accept()
