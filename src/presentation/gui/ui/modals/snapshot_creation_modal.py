from typing import Callable

from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

from src.presentation.gui.ui.modals import ErrorNotificationModal


class SnapshotCreationModal(QDialog):
    def __init__(self, on_submit: Callable[[str, str], None]):
        super().__init__()
        self.setWindowTitle("Create Snapshot")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Snapshot name")

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Optional description")

        submit_btn = QPushButton("Create")
        submit_btn.clicked.connect(self._submit)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

        self.on_submit = on_submit

    def _submit(self):
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()
        if not name:
            ErrorNotificationModal("Snapshot name is required").exec()
            return
        self.accept()
        self.on_submit(name, description)