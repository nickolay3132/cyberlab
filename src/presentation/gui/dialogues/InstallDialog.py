from typing import List

from PyQt6 import QtWidgets

from src.presentation.gui.RunTerminalCommand import RunTerminalCommand
from src.presentation.gui.dialogues.Dialog import Dialog


class InstallDialog(Dialog):
    skip_download: QtWidgets.QCheckBox
    no_verify: QtWidgets.QCheckBox

    def __init__(self, cmd: List[str], command_executor: RunTerminalCommand, parent=None):
        super().__init__(cmd, command_executor, parent)
        self.setWindowTitle("Install Parameters")
        self.cmd.extend(["install"])


    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.skip_download = QtWidgets.QCheckBox("SKip download")
        self.no_verify = QtWidgets.QCheckBox("No verify ova files checksum")

        layout.addWidget(self.skip_download)
        layout.addWidget(self.no_verify)

        layout.addLayout(self.buttons_layout())

    def execute(self):
        if self.skip_download.isChecked():
            self.cmd.extend(["--skip-download"])

        self.command_executor.exec(self.cmd)
        self.accept()