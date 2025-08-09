from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QPushButton


class ErrorNotificationModal(QDialog):
    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        self._setup_ui(message)
        self._configure_window()

    def _setup_ui(self, message):
        layout = QVBoxLayout()

        error_label = QLabel(message)
        error_label.setStyleSheet("""
            QLabel {
                color: #d32f2f;
                font-weight: bold;
                padding: 10px;
                min-width: 300px;
            }
        """)
        error_label.setWordWrap(True)
        layout.addWidget(error_label)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.adjustSize()

    def _configure_window(self):
        self.setWindowTitle('Error')
        self.setWindowIcon(QIcon(":/icons/error.png"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowCloseButtonHint
        )

    # def show(self):
    #     super().show()
    #     self._center_on_screen()
    #
    # def _center_on_screen(self):
    #     screen = QApplication.primaryScreen().availableGeometry()
    #     x = (screen.width() - self.width()) // 2
    #     y = (screen.height() - self.height()) // 2
    #     self.move(x, y)