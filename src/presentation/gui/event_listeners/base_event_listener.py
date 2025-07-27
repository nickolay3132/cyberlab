import time
from enum import Enum
from typing import Dict, Callable, List, Optional, Literal, Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from src.core.entities.event_bus import Event, EventListener
from src.presentation.gui.event_listeners import EventListenerGuiSignalBridge


class BaseEventListener[E: Event](EventListener[E]):
    def __init__(self, layout_map: Dict[str, QVBoxLayout]):
        self._layout_map = layout_map
        self._signal = EventListenerGuiSignalBridge[E](self._handle_event)

        self._event_handlers: Dict[str | Enum, Callable[[E], QWidget]] = {}
        self._skip_clear_for_events: List[str | Enum] = []

    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        time.sleep(3)
        for layout in self._layout_map.values():
            self._clear_layout(layout)

    def on_event(self, event: E) -> None:
        self._signal.emit(event)

    def add_event_handlers(self, handler: Dict[str | Enum, Callable[[E], QWidget]]):
        self._event_handlers.update(handler)

    def add_skip_clear_for_event(self, event_type: str | Enum) -> None:
        self._skip_clear_for_events.append(event_type)

    def _handle_event(self, event: E):
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

    def unknown_event(self, event: E):
        return None