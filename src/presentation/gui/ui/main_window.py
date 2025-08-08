from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QPalette, QColor
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
        self.central_widget = QWidget()

        layout = self._layout()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        MainController(self._set_central_widget).show_main_page()

    def _set_central_widget(self, widget: QWidget):
        layout = self.central_widget.layout()

        if layout is None:
            layout = QVBoxLayout(self.central_widget)

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Добавить новый виджет
        layout.addWidget(widget)

    def _layout(self) -> QLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.topbar, stretch=0)
        layout.addWidget(self.central_widget, stretch=1)
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
        StartupController(self._set_central_widget).show_startup_page()

    def on_shutdown_clicked(self):
        ShutdownController(self._set_central_widget).show_shutdown_page()
