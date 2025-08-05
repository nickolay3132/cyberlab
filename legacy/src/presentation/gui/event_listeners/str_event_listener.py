from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

from src.core.entities.event_bus.events import StrEvent, StrEventTypes
from src.presentation.gui.event_listeners import BaseEventListener


class StrEventListener(BaseEventListener[StrEvent]):
    def __init__(self, layout_map):
        super().__init__(layout_map)

        self.font = QFont("Courier", 11)
        self.alignment = Qt.AlignmentFlag.AlignLeft

        self.add_event_handlers({
            StrEventTypes.TITLE: self.title_event,
            StrEventTypes.SUCCESS: self.success_event,
            StrEventTypes.TEXT: self.text_event,
            StrEventTypes.WARNING: self.warning_event,
            StrEventTypes.ERROR: self.error_event,
        })

    def title_event(self, event: StrEvent):
        label = QLabel(f"<span style='color: cyan;'>{event.data}</span>")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def success_event(self, event: StrEvent):
        label = QLabel(f"<span style='color: green;'>{event.data}</span>")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def text_event(self, event: StrEvent):
        label = QLabel(f"<span style=''>{event.data}</span>")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def warning_event(self, event: StrEvent):
        label = QLabel(f"<span style='color: yellow;'>Warning:</span> {event.data}")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label

    def error_event(self, event: StrEvent):
        label = QLabel(f"<span style='color: red;'>Error:</span> {event.data}")
        label.setFont(self.font)
        label.setAlignment(self.alignment)
        return label