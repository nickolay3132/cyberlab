import threading

from PyQt6 import QtWidgets

from src.core.use_cases.vm_commands.ShutdownUseCase import ShutdownUseCaseDTO
from src.presentation.gui.dialogues.Dialog import Dialog


class ShutdownDialog(Dialog):
    shutdown_force: QtWidgets.QCheckBox

    def __init__(self, use_cases, parent=None):
        super().__init__(use_cases, parent)
        self.setWindowTitle("Shutdown Parameters")

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.shutdown_force = QtWidgets.QCheckBox("Shutdown force")
        layout.addWidget(self.shutdown_force)
        layout.addLayout(self.buttons_layout())

    def execute(self):
        if self.shutdown_force.isChecked():
            pass

        shutdown_use_case = self.use_cases.shutdown_use_case()
        dto = ShutdownUseCaseDTO(
            force=self.shutdown_force.isChecked(),
        )

        def runner():
            shutdown_use_case.execute(dto)

        thread = threading.Thread(target=runner)
        thread.start()
        self.accept()
