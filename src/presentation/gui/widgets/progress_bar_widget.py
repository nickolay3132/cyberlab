from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar

from src.core.entities.progress_bar_data import ProgressBarData, ProgressBarStates

from PyQt6.QtWidgets import (QProgressBar, QWidget, QHBoxLayout,
                             QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ProgressBarWidget(QWidget):
    def __init__(self, download_id: str, parent=None):
        super().__init__(parent)
        self.download_id = download_id
        self.init_ui()

    def init_ui(self):
        # Основной вертикальный layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Горизонтальный layout для прогресс-бара и процентов
        self.progress_layout = QHBoxLayout()
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_layout.setSpacing(10)  # Отступ между элементами

        # Label перед прогресс-баром
        self.status_label = QLabel("Downloading:")
        self.status_label.setFont(QFont("Courier", 11))

        # Сам прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)  # Скрываем текст внутри бара

        # Label для отображения процентов
        self.percent_label = QLabel("0%")
        self.percent_label.setFont(QFont("Arial", 9))
        self.percent_label.setMinimumWidth(40)  # Фиксированная ширина для выравнивания

        # Добавляем элементы в горизонтальный layout
        self.progress_layout.addWidget(self.status_label)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.percent_label)

        # Добавляем горизонтальный layout в основной
        self.main_layout.addLayout(self.progress_layout)

        # Начальное состояние
        self.update_progress(ProgressBarData(state=ProgressBarStates.INIT))

    def update_progress(self, data: ProgressBarData):
        if data.state == ProgressBarStates.INIT:
            self.progress_bar.setValue(0)
            self.status_label.setText("Waiting...")
            self.percent_label.setText("0%")
            self.progress_bar.setRange(0, 100)

        elif data.state == ProgressBarStates.IN_PROGRESS:
            self.status_label.setText("Downloading:")

            if data.total > 0:
                progress = int((data.actual / data.total) * 100)
                self.progress_bar.setValue(progress)
                self.percent_label.setText(f"{progress}%")
                self.progress_bar.setRange(0, 100)
            else:
                # Если общий размер неизвестен
                self.progress_bar.setRange(0, 0)  # Индикатор занятости
                self.percent_label.setText("...")

        elif data.state == ProgressBarStates.COMPLETED:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(100)
            self.status_label.setText("Completed!")
            self.percent_label.setText("100%")

        elif data.state == ProgressBarStates.ERROR:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.status_label.setText("Error:")
            self.percent_label.setText(data.error_msg or "Unknown error")