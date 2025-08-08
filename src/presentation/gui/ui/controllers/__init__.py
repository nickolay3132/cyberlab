from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtSlot


running_threads = []

class UseCaseWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, usecase, dto):
        super().__init__()
        self.usecase = usecase
        self.dto = dto

    @pyqtSlot()
    def run(self):
        self.usecase.execute(self.dto)
        self.finished.emit()

def run_usecase_async(usecase, dto, on_complete):
    thread = QThread()
    worker = UseCaseWorker(usecase, dto)
    worker.moveToThread(thread)

    thread.started.connect(worker.run)
    worker.finished.connect(on_complete)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    worker.finished.connect(thread.deleteLater)

    thread.start()

    running_threads.append((thread, worker))


from .main_controller import MainController
from .startup_controller import StartupController
