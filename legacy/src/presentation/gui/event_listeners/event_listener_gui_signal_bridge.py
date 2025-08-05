from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from src.core.entities.event_bus import Event


class EventListenerGuiSignalBridge[E: Event](QObject):
    _update_signal = pyqtSignal(object)

    def __init__(self, handler: Callable[[E], None]):
        super().__init__()
        self.moveToThread(QApplication.instance().thread())
        self._update_signal.connect(handler)

    def emit(self, event: E):
        self._update_signal.emit(event)