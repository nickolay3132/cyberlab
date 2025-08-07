import uuid

from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer

running_threads = []

class UseCaseWorker(QObject):
    finished = pyqtSignal()
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        self.fn()
        self.finished.emit()

def run_usecase_async(fn, on_complete):
    thread = QThread()
    worker = UseCaseWorker(fn)
    worker.moveToThread(thread)
    worker.finished.connect(on_complete)
    thread.started.connect(worker.run)
    thread.start()

    running_threads.append((thread, worker))

from .main_controller import MainController
from .startup_controller import StartupController
