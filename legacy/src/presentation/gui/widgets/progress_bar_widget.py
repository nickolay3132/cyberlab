from PyQt6.QtWidgets import (QProgressBar, QWidget, QHBoxLayout,
                             QLabel, QVBoxLayout, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ProgressBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 15)
        self.main_layout.setSpacing(0)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_layout.setSpacing(5)

        self.status_label = QLabel("Waiting...")
        self.status_label.setFont(QFont("Courier", 11))
        self.status_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.percent_label = QLabel("0%")
        self.percent_label.setFont(QFont("Arial", 9))
        self.percent_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.progress_layout.addWidget(self.status_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.percent_label)

        self.main_layout.addLayout(self.progress_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.progress_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setFixedHeight(30)

        self.init()

    def init(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.status_label.setText("Waiting...")
        self.percent_label.setText("0%")

    def update_progress(self, total: int, actual: int):
        self.status_label.setText("Downloading:")
        if total > 0:
            progress = int((actual / total) * 100)
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(progress)
            self.percent_label.setText(f"{progress}%")
        else:
            self.progress_bar.setRange(0, 0)
            self.percent_label.setText("...")

    def completed(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.status_label.setText("Completed!")
        self.percent_label.setText("100%")

    def error(self, error_message: str):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.status_label.setText("Error:")
        self.percent_label.setText(error_message or "Unknown error")