import threading

from PyQt6 import QtWidgets

from src.core.use_cases.vm_commands.InstallUseCase import InstallUseCaseDTO
from src.presentation.gui.dialogues.Dialog import Dialog


class InstallDialog(Dialog):
    skip_download: QtWidgets.QCheckBox
    no_verify: QtWidgets.QCheckBox

    def __init__(self, use_cases, parent=None):
        super().__init__(use_cases, parent)
        self.setWindowTitle("Install Parameters")


    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.skip_download = QtWidgets.QCheckBox("SKip download")
        self.no_verify = QtWidgets.QCheckBox("No verify ova files checksum")

        layout.addWidget(self.skip_download)
        layout.addWidget(self.no_verify)

        layout.addLayout(self.buttons_layout())

    def execute(self):
        install_use_case = self.use_cases.install_use_case()

        dto = InstallUseCaseDTO(
            skip_download=self.skip_download.isChecked(),
            no_verify=self.no_verify.isChecked(),
        )

        def runner():
            install_use_case.execute(dto)

        thread = threading.Thread(target=runner)
        thread.start()
        self.accept()