from typing import Tuple, Dict, List

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from src.bootstrap import global_vars
from src.core.entities.event_bus.events import TextEvent, VmsListEvent


class VmsStatusPanel(QWidget):
    rows_signal = pyqtSignal(object)
    text_event_signal = pyqtSignal(TextEvent)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        # vm_name -> (row_layout, content_widget)
        self.rows: Dict[str, Tuple[QHBoxLayout, QWidget]] = {}
        self.font = global_vars.get('font', QFont())

        self.rows_signal.connect(self._render_rows_handler)
        self.text_event_signal.connect(self._update_text_handler)

    def render_rows(self, rows_titles: List[str]) -> None:
        self.rows_signal.emit(rows_titles)

    def update_text(self, text: TextEvent) -> None:
        self.text_event_signal.emit(text)

    def _render_rows_handler(self, rows_titles: List[str]) -> None:
        for row_title in rows_titles:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            formatted_vm_name = '-'.join(part.capitalize() for part in row_title.split('-'))
            name_label = QLabel(f'{formatted_vm_name}: ')
            name_label.setFont(self.font)

            content_widget = QLabel("")

            if row_title != 'main':
                row_layout.addWidget(name_label)
            row_layout.addWidget(content_widget)

            container = QWidget()
            container.setLayout(row_layout)

            self.layout.addWidget(container)
            self.rows[row_title] = (row_layout, content_widget)

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