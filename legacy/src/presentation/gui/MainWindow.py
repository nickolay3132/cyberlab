from typing import Any, Dict, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea, QGridLayout, QPushButton
import pyfiglet

import src
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository
from src.presentation.gui.widgets.statuses_panel import StatusesPanel


class MainWindow(QWidget):
    def __init__(self,
                 vms_repository: VirtualMachinesRepository,
                 buttons: Dict[str, Any],
                 callback: Callable[[str], None]):
        super().__init__()
        self.setWindowTitle("CyberLab Management Tool")
        self.setMinimumSize(600, 300)

        self.vms_repository = vms_repository

        self.statuses_panel = StatusesPanel(self._get_layout_fields(), self)
        self.app_version = src.__version__
        self.buttons = buttons
        self.callback = callback

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self._get_art_label())

        layout.addWidget(self.statuses_panel, stretch=1)

        scroll = QScrollArea()
        scroll.setWidget(self._get_buttons_grid())
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

    def _get_art_label(self) -> QLabel:
        art_label = QLabel(self._show_gui_header(self.app_version))
        art_label.setFont(QFont("Courier", 10))
        art_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        art_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return art_label

    def _get_buttons_grid(self) -> QWidget:
        button_container = QWidget()
        grid_layout = QGridLayout(button_container)

        cols = 5

        for i, label in enumerate(self.buttons):
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, text=label: self.callback(text))
            grid_layout.addWidget(btn, i // cols, i % cols)

        return button_container

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

    def _get_layout_fields(self):
        layout_fields = ['Main']

        for vm in self.vms_repository.get_all():
            layout_fields.append('-'.join(word.capitalize() for word in vm.name.split('-')))

        return layout_fields

