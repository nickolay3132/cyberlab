from PyQt6.QtCore import pyqtSignal, QThread


running_threads = []

class UseCaseWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, usecase, dto):
        super().__init__()
        self.usecase = usecase
        self.dto = dto

    def run(self):
        self.usecase.execute(self.dto)
        self.finished.emit()

def run_usecase_async(usecase, dto, on_complete):
    worker = UseCaseWorker(usecase, dto)
    worker.finished.connect(on_complete)
    worker.start()

    running_threads.append((None, worker))

from .install_controller import install_controller
from .main_controller import main_controller
from .shutdown_controller import shutdown_controller
from .startup_controller import startup_controller
