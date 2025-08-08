import functools
from typing import Callable

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLayout, QHBoxLayout, QPushButton, QSizePolicy, QApplication

from src.bootstrap import global_vars


class TopBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = self._layout()
        self.font = global_vars.get('btn_font', QFont())

        self.buttons = []

    def _layout(self) -> QLayout:
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)
        return layout

    def add_button(self, text: str, callback: Callable[[], None]) -> None:
        btn = QPushButton(text)
        btn.setFont(self.font)
        btn.setStyleSheet("padding: 8px 16px;")
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(functools.partial(self._handle_click, callback))
        self.buttons.append(btn)
        self.layout.addWidget(btn)

        self.buttons.append(btn)

    def disable_buttons(self) -> None:
        for btn in self.buttons:
            btn.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, False)
            btn.clearFocus()
            btn.setEnabled(False)
            btn.repaint()

    def enable_buttons(self) -> None:
        for btn in self.buttons:
            btn.setEnabled(True)

    @staticmethod
    def _handle_click(callback) -> None:
        callback()
