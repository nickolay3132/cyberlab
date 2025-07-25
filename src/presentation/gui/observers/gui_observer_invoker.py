import time
from typing import Dict, List, Callable, Optional

from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget

from src.core.entities.observer import Observer, ObserverEvent


class GUISignalBridge(QObject):
    _update_signal = pyqtSignal(object)

    def __init__(self, handler: Callable[[ObserverEvent], None]):
        super().__init__()
        self.moveToThread(QApplication.instance().thread())
        self._update_signal.connect(handler)

    def emit(self, event: ObserverEvent):
        self._update_signal.emit(event)


class GUIObserverInvoker(Observer):
    def __init__(self, layout_map: Dict[str, QVBoxLayout]):
        self._layout_map = layout_map
        self._signal = GUISignalBridge(self._handle_update)

        self._event_handlers: Dict[str, Callable[[ObserverEvent], QWidget]] = {}
        self._skip_clear_for_events: List[str] = []

    def update(self, event: ObserverEvent):
        self._signal.emit(event)

    def on_detach(self) -> None:
        time.sleep(3)
        for layout in self._layout_map.values():
            self._clear_layout(layout)

    def add_event_handlers(self, handler: Dict[str, Callable[[ObserverEvent], QWidget]]):
        self._event_handlers.update(handler)

    def add_skip_clear_for_event(self, event_type: str):
        self._skip_clear_for_events.append(event_type)

    def _handle_update(self, event: ObserverEvent):
        if event.id not in self._layout_map:
            return

        layout = self._layout_map[event.id]
        if not event.type in self._skip_clear_for_events and event.type in self._event_handlers.keys():
            self._clear_layout(layout)

        widget = self._create_widget_for_event(event)
        if widget is None:
            return

        layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignTop)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
                item.layout().deleteLater()

    def _create_widget_for_event(self, event) -> Optional[QWidget]:
        handler = self._event_handlers.get(event.type, self.unknown_event)
        return handler(event)

    def unknown_event(self, event: ObserverEvent):
        return None