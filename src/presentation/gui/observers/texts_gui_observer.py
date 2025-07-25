from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel

from src.core.entities.observer import ObserverEvent
from src.presentation.gui.observers.gui_observer_invoker import GUIObserverInvoker


class TextsGuiObserver(GUIObserverInvoker):
    def __init__(self, layout_map: Dict[str, QVBoxLayout]):
        super().__init__(layout_map)

        self.font = QFont("Courier", 11)
        self.alignment = Qt.AlignmentFlag.AlignLeft
        self.add_event_handlers({
            "title": self.title_event,
            "success": self.success_event,
            "text": self.text_event,
            "warning": self.warning_event,
            "error": self.error_event,
        })

    def title_event(self, event: ObserverEvent):
        label = QLabel(f"<span style='color: cyan;'>{event.data}</span>")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def success_event(self, event: ObserverEvent):
        label = QLabel(f"<span style='color: green;'>{event.data}</span>")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def text_event(self, event: ObserverEvent):
        label = QLabel(f"<span style=''>{event.data}</span>")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def warning_event(self, event: ObserverEvent):
        label = QLabel(f"<span style='color: yellow;'>Warning:</span> {event.data}")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def error_event(self, event: ObserverEvent):
        label = QLabel(f"<span style='color: red;'>Error:</span> {event.data}")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label