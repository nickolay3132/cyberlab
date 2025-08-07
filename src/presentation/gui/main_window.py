from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, \
    QLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberLab Management Tool")
        self.setMinimumSize(800, 600)

        self.topbar = self._topbar()
        self.stack = QStackedWidget()

        layout = self._layout()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


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
        btn_startup.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_startup.clicked.connect(self.on_startup_clicked)
        topbar_layout.addWidget(btn_startup)

        #  other buttons

        topbar.setLayout(topbar_layout)
        return topbar

    def on_startup_clicked(self):
        print("startup clicked")