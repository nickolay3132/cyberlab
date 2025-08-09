import functools

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLayout

from src.bootstrap import global_vars
from src.presentation.gui.controllers import MainController, StartupController
from src.presentation.gui.controllers.install_controller import InstallController
from src.presentation.gui.controllers.shutdown_controller import ShutdownController
from src.presentation.gui.ui.widgets import TopBarWidget


class MainWindow(QMainWindow):
    controllers = {
        'main': MainController,
        'install': InstallController,
        'startup': StartupController,
        'shutdown': ShutdownController,
    }

    buttons = ['Install', 'Startup', 'Shutdown']
    font = global_vars.get('btn_font', QFont())

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberLab Management Tool")
        self.setMinimumSize(800, 600)

        self.topbar = TopBarWidget()
        for btn_label in self.buttons:
            self.topbar.add_button(btn_label, functools.partial(self._run_controller, btn_label))


        self.central_widget = QWidget()

        layout = self._layout()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self._run_controller('main')

    def _set_central_widget(self, widget: QWidget):
        layout = self.central_widget.layout()

        if layout is None:
            layout = QVBoxLayout(self.central_widget)

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        layout.addWidget(widget)

    def _layout(self) -> QLayout:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.topbar, stretch=0)
        layout.addWidget(self.central_widget, stretch=1)
        return layout

    def _run_controller(self, key: str) -> None:
        controller = self.controllers.get(key.lower(), None)

        if controller:
            self.topbar.disable_buttons()
            controller(self._set_central_widget, self.topbar.enable_buttons).run()

