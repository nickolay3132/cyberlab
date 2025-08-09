from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar


class ProgressBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.total = 0

        self.layout = QVBoxLayout(self)
        self.progress_bar = QProgressBar(self)

        # Unified style across platforms
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Optional: consistent height and style
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 5px;
                background-color: #222;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00aaee;
                width: 1px;
            }
        """)

        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

    def init_progress(self, total: int) -> None:
        self.total = total
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

    def update_progress(self, actual: int) -> None:
        percent = int(actual / self.total * 100)
        self.progress_bar.setValue(percent)

    def complete(self) -> None:
        self.progress_bar.setValue(self.progress_bar.maximum())

    def close_progress(self) -> None:
        self.setParent(None)
        self.deleteLater()