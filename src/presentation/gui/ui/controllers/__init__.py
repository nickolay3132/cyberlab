from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtSlot


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
    # thread = QThread()
    # worker = UseCaseWorker(usecase, dto)
    # worker.moveToThread(thread)
    #
    # thread.started.connect(worker.run)
    # worker.finished.connect(on_complete)
    # worker.finished.connect(thread.quit)
    # worker.finished.connect(worker.deleteLater)
    # worker.finished.connect(thread.deleteLater)

    worker = UseCaseWorker(usecase, dto)
    worker.finished.connect(on_complete)
    worker.start()

    # thread.start()

    # def cleanup():
    #     if (thread, worker) in running_threads:
    #         running_threads.remove((thread, worker))
    #
    # thread.finished.connect(cleanup)

    running_threads.append((None, worker))


from .main_controller import MainController
from .startup_controller import StartupController
