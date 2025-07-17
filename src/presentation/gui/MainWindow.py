from typing import Any, Dict, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea, QGridLayout, QPushButton
import pyfiglet

import src


class MainWindow(QWidget):
    def __init__(self, buttons: Dict[str, Any], callback: Callable[[str], None]):
        super().__init__()
        self.setWindowTitle("CyberLab Management Tool")
        self.setMinimumSize(400, 180)

        self.app_version = src.__version__

        self.buttons = buttons
        self.callback = callback

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        art_label = QLabel(self._show_gui_header(self.app_version))
        art_label.setFont(QFont("Courier", 10))
        art_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        art_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(art_label)

        scroll = QScrollArea()
        button_container = QWidget()
        grid_layout = QGridLayout(button_container)

        cols = 5

        for i, label in enumerate(self.buttons):
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, text=label: self.callback(text))
            grid_layout.addWidget(btn, i // cols, i % cols)

        scroll.setWidget(button_container)
        scroll.setWidgetResizable(True)

        layout.addWidget(scroll)

    @staticmethod
    def _show_gui_header(version: str):
        ascii_title = pyfiglet.figlet_format("CyberLab", font="slant")
        description = "Cyber Lab management tool"
        version = version.rjust(55)



        header = f"""
        <pre><font color="cyan">{ascii_title}</font></pre>
        {"━" * 18}
        {description}
        <pre><font color="yellow">{version}</font></pre>
        """

        return header