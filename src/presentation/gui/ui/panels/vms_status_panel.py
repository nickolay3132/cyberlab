from typing import Tuple, Dict, List

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy

from src.bootstrap import global_vars
from src.core.entities.event_bus.events import TextEvent


class VmsStatusPanel(QWidget):
    text_event_signal = pyqtSignal(TextEvent)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)  # необязательно, но красиво
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # ← к
        self.setLayout(self.layout)

        # vm_name -> (row_layout, content_widget)
        self.rows: Dict[str, Tuple[QHBoxLayout, QWidget]] = {}
        self.font = global_vars.get('font', QFont())

        self.text_event_signal.connect(self._update_text_handler)

    def initialize(self, vm_names: List[str]) -> None:
        for vm_name in vm_names:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)  # убираем промежутки между виджетами
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # прижимаем весь ряд влево

            formatted_vm_name = '-'.join(part.capitalize() for part in vm_name.split('-'))
            name_label = QLabel(f'{formatted_vm_name}: ')
            name_label.setFont(self.font)

            content_widget = QLabel("")

            row_layout.addWidget(name_label)
            row_layout.addWidget(content_widget)

            container = QWidget()
            container.setLayout(row_layout)

            self.layout.addWidget(container)
            self.rows[vm_name] = (row_layout, content_widget)

    def update_text(self, text: TextEvent) -> None:
        self.text_event_signal.emit(text)

    def _update_text_handler(self, event: TextEvent):
        if event.id not in self.rows:
            return

        row_layout, old_widget = self.rows[event.id]
        row_layout.removeWidget(old_widget)
        old_widget.deleteLater()

        new_widget = QLabel(event.text)
        new_widget.setFont(self.font)
        row_layout.addWidget(new_widget)
        self.rows[event.id] = (row_layout, new_widget)