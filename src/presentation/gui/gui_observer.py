from typing import Dict, List

from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QApplication

from src.core.entities.observer import Observer, ObserverEvent
from src.presentation.gui.widgets.progress_bar_widget import ProgressBarWidget


class GUISignalBridge(QObject):
    update_signal = pyqtSignal(object)

class GUIObserver(Observer):
    def __init__(self, label_map: Dict[str, QVBoxLayout]):
        self.label_map = label_map
        self.signal = GUISignalBridge()
        self.signal.moveToThread(QApplication.instance().thread())
        self.signal.update_signal.connect(self._handle_update)

        self.max_logs = 4
        self.buffers: Dict[str, List[QLabel | ProgressBarWidget]] = {
            vm: [] for vm in label_map
        }

    def update(self, event: ObserverEvent):
        # Просто отправляем событие в главный поток
        self.signal.update_signal.emit(event)

    def _handle_update(self, event: ObserverEvent):
        if event.id not in self.label_map:
            return

        layout = self.label_map[event.id]

        if not event.type == 'progress':
            self._clear_layout(layout)

        widget = self._create_widget_for_event(event)
        if widget is None:
            return

        layout.addWidget(widget)

        self.buffers[event.id] = [widget]

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
                item.layout().deleteLater()

    def _create_widget_for_event(self, event):
        match event.type:
            case "title":
                return self._create_label(event.data)
            case "error":
                return self._create_label(f"ERROR: {event.data}")
            case "success":
                return self._create_label(f"Success: {event.data}")
            case "warning":
                return self._create_label(f"Warning: {event.data}")
            case "text":
                return self._create_label(f"{event.data}")
            case "progress":
                if not hasattr(self, 'progress_bars'):
                    self.progress_bars = {}

                if event.id not in self.progress_bars:
                    self.progress_bars[event.id] = ProgressBarWidget(download_id=event.id)

                self.progress_bars[event.id].update_progress(event.data)
                return self.progress_bars[event.id]
            case _:
                return None

    def _create_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Courier", 11))
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return label