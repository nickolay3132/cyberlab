from typing import List, Dict, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy


class StatusesPanel(QWidget):
    def __init__(self, vm_ids: List[str], parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.vm_logs: Dict[str, QVBoxLayout] = {}

        for label_text in vm_ids:
            if label_text == "Main":
                continue

            row_container, content_layout = self._get_row(label_text)
            self.vm_logs[label_text.lower()] = content_layout
            self.layout.addWidget(row_container)

        label = QLabel()
        label.setFont(QFont("Courier", 11))
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        label_container = QWidget()
        v_layout = QVBoxLayout(label_container)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        v_layout.setContentsMargins(0, 5, 0, 0)
        v_layout.addWidget(label)

        main_layout = QVBoxLayout()
        self.layout.addLayout(main_layout)

        self.vm_logs['main'] = main_layout

    def _get_row(self, label_text: str) -> Tuple[QWidget, QVBoxLayout]:
        row_container = QWidget()
        row_container.setMinimumHeight(30)
        row_layout = QHBoxLayout(row_container)
        row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        row_layout.setSpacing(5)
        row_layout.setContentsMargins(0, 0, 0, 0)

        row_label = self._get_row_label(label_text)
        content_container, content_layout = self._get_content_container()

        row_layout.addWidget(row_label)
        row_layout.addWidget(content_container, stretch=1)
        row_layout.setAlignment(row_label, Qt.AlignmentFlag.AlignTop)
        row_layout.setAlignment(content_container, Qt.AlignmentFlag.AlignTop)

        return row_container, content_layout


    @staticmethod
    def _get_row_label(label_text: str) -> QLabel:
        vm_label = QLabel(f"{label_text}:")
        vm_label.setFont(QFont("Courier", 11))
        vm_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        vm_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        return vm_label

    @staticmethod
    def _get_content_container() -> Tuple[QWidget, QVBoxLayout]:
        content_container = QWidget()
        content_container.setMinimumHeight(30)
        content_layout = QVBoxLayout(content_container)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        return content_container, content_layout