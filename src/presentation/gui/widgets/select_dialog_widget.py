from PyQt6.QtWidgets import (
    QDialog, QButtonGroup, QVBoxLayout, QLabel,
    QRadioButton, QHBoxLayout, QPushButton
)


class SelectDialogWidget(QDialog):
    def __init__(self, options, future, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Выберите вариант")
        self.setModal(True)

        self.options = options
        self.future = future
        self.button_group = QButtonGroup(self)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Пожалуйста, выберите один вариант:"))

        for idx, option in enumerate(self.options):
            radio = QRadioButton(option)
            self.button_group.addButton(radio, idx)
            layout.addWidget(radio)

        button_layout = QHBoxLayout()
        accept_btn = QPushButton("Принять")
        exit_btn = QPushButton("Отмена")

        accept_btn.clicked.connect(self._accept_clicked)
        exit_btn.clicked.connect(self._exit_clicked)

        button_layout.addWidget(accept_btn)
        button_layout.addWidget(exit_btn)
        layout.addLayout(button_layout)

    def _accept_clicked(self):
        checked_id = self.button_group.checkedId()
        if checked_id != -1 and self.future and not self.future.done():
            self.future.set_result(checked_id)
        self.close()

    def _exit_clicked(self):
        if self.future and not self.future.done():
            self.future.set_result(None)
        self.close()

    def closeEvent(self, event):
        if self.future and not self.future.done():
            self.future.set_result(None)
        super().closeEvent(event)
