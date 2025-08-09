from typing import Tuple, Dict, List

from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication

from src.bootstrap import global_vars
from src.core.entities.event_bus.events import TextEvent, VmsListEvent, ProgressEvent
from src.core.enums import DownloadingType
from src.core.enums.events import TextEventType
from src.presentation.gui.ui.modals import ErrorNotificationModal
from src.presentation.gui.ui.widgets import ProgressBarWidget


class VmsStatusPanel(QWidget):
    rows_signal = pyqtSignal(object)
    text_event_signal = pyqtSignal(TextEvent)
    progress_bar_signal = pyqtSignal(ProgressEvent)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        # self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        # vm_name -> (row_layout, content_widget)
        self.rows: Dict[str, Tuple[QHBoxLayout, QWidget]] = {}
        self.font = global_vars.get('font', QFont())

        self.rows_signal.connect(self._render_rows_handler)
        self.text_event_signal.connect(self._update_text_handler)
        self.progress_bar_signal.connect(self._progress_bar_handler)

    def render_rows(self, rows_titles: List[str]) -> None:
        self.rows_signal.emit(rows_titles)

    def update_text(self, text: TextEvent) -> None:
        self.text_event_signal.emit(text)

    def progress_bar(self, event: ProgressEvent) -> None:
        self.progress_bar_signal.emit(event)

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
        if event.id == 'dialog' and event.type == TextEventType.ERROR:
            self.open_modal(event.text)

        if event.id not in self.rows:
            return

        row_layout, old_widget = self.rows[event.id]
        row_layout.removeWidget(old_widget)
        old_widget.deleteLater()

        new_widget = QLabel("")

        if event.type == TextEventType.TITLE:
            new_widget.setText(f"<span style='color: cyan;'>{event.text}</span>")
        elif event.type == TextEventType.SUCCESS:
            new_widget.setText(f"<span style='color: green;'>{event.text}</span>")
        elif event.type == TextEventType.WARNING:
            new_widget.setText(f"<span style='color: yellow;'>{event.text}</span>")
        elif event.type == TextEventType.ERROR:
            new_widget.setText(f"<span style='color: red;'>{event.text}</span>")
        else:
            new_widget.setText(event.text)

        new_widget.setFont(self.font)
        row_layout.addWidget(new_widget)
        self.rows[event.id] = (row_layout, new_widget)

    def _progress_bar_handler(self, event: ProgressEvent):
        if event.id not in self.rows:
            return

        row_layout, old_widget = self.rows[event.id]

        if event.type == DownloadingType.INIT:
            row_layout.removeWidget(old_widget)
            old_widget.deleteLater()

            progress_widget = ProgressBarWidget()
            progress_widget.init_progress(event.total)

            row_layout.addWidget(progress_widget)
            self.rows[event.id] = (row_layout, progress_widget)
            return

        if event.type == DownloadingType.IN_PROGRESS and isinstance(old_widget, ProgressBarWidget):
            old_widget.update_progress(event.actual)
            return

        if event.type == DownloadingType.COMPLETED and isinstance(old_widget, ProgressBarWidget):
            row_layout.removeWidget(old_widget)
            old_widget.deleteLater()

            new_widget = QLabel(f"<span style='color: green;'>vm downloaded</span>")
            new_widget.setFont(self.font)
            row_layout.addWidget(new_widget)
            self.rows[event.id] = (row_layout, new_widget)
            return

        if event.type == DownloadingType.FAILED:
            row_layout.removeWidget(old_widget)
            old_widget.deleteLater()

            new_widget = QLabel(f"<span style='color: red;'>unable to download vm</span>")
            new_widget.setFont(self.font)
            row_layout.addWidget(new_widget)
            self.rows[event.id] = (row_layout, new_widget)
            self.open_modal(event.error_msg)
            return

    @staticmethod
    def open_modal(text: str) -> None:
        QApplication.processEvents()
        QTimer.singleShot(0, lambda: ErrorNotificationModal(text).exec())