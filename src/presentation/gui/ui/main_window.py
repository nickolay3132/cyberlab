from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, \
    QLayout

from src.bootstrap import global_vars
from src.presentation.gui.ui.controllers import MainController, StartupController
from src.presentation.gui.ui.controllers.shutdown_controller import ShutdownController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.font = global_vars.get('btn_font', QFont())

        self.setWindowTitle("CyberLab Management Tool")
        self.setMinimumSize(800, 600)

        self.topbar = self._topbar()
        self.stack = QStackedWidget()

        layout = self._layout()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        MainController(self.stack).show_main_page()


    def _layout(self) -> QLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.topbar)
        layout.addWidget(self.stack)
        return layout

    def _topbar(self) -> QWidget:
        topbar = QWidget()
        topbar_layout = QHBoxLayout()
        topbar_layout.setContentsMargins(10, 10, 10, 10)
        topbar_layout.setSpacing(15)

        btn_startup = QPushButton("Startup")
        btn_startup.setFont(self.font)
        btn_startup.setStyleSheet("padding: 8px 16px;")
        btn_startup.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_startup.clicked.connect(self.on_startup_clicked)
        topbar_layout.addWidget(btn_startup)

        btn_shutdown = QPushButton("Shutdown")
        btn_shutdown.setFont(self.font)
        btn_shutdown.setStyleSheet("padding: 8px 16px;")
        btn_shutdown.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_shutdown.clicked.connect(self.on_shutdown_clicked)
        topbar_layout.addWidget(btn_shutdown)

        topbar.setLayout(topbar_layout)
        return topbar

    def on_startup_clicked(self):
        StartupController(self.stack).show_startup_page()

    def on_shutdown_clicked(self):
        ShutdownController(self.stack).show_shutdown_page()
