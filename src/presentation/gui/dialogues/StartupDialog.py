import threading

from PyQt6 import QtWidgets

from src.core.use_cases.vm_commands.StartupUseCase import StartupUseCaseDTO
from src.presentation.gui.dialogues.Dialog import Dialog


class StartupDialog(Dialog):
    def __init__(self, use_cases, observers, parent=None):
        super().__init__(use_cases, observers, parent)
        self.setWindowTitle("Startup Parameters")

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(self.buttons_layout())

    def execute(self):
        startup_use_case = self.use_cases.startup_use_case()
        [startup_use_case.subject.attach(observer) for observer in self.observers]
        dto = StartupUseCaseDTO()

        def runner():
            startup_use_case.execute(dto)

        thread = threading.Thread(target=runner)
        thread.start()
        self.accept()

