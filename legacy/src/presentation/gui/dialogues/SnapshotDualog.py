import threading

from PyQt6 import QtWidgets

from src.core.use_cases.snapshots.CreateSnapshotUseCase import CreateSnapshotUseCaseDTO
from src.core.use_cases.snapshots.ListSnapshotsUseCase import ListSnapshotsUseCaseDTO
from src.core.use_cases.snapshots.RestoreSnapshotUseCase import RestoreSnapshotUseCaseDTO
from src.presentation.gui.dialogues.Dialog import Dialog


class SnapshotDialog(Dialog):
    subcommand_selector: QtWidgets.QComboBox

    top_container: QtWidgets.QWidget
    bottom_container: QtWidgets.QWidget

    name_container: QtWidgets.QWidget
    name_label: QtWidgets.QLabel
    name_input: QtWidgets.QLineEdit

    description_container: QtWidgets.QWidget
    description_label: QtWidgets.QLabel
    description_input: QtWidgets.QLineEdit

    def __init__(self, use_cases, parent=None):
        super().__init__(use_cases, parent)
        self.setWindowTitle("Manage Snapshots")

        self.use_case = None
        self.dto = None

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.setup_top_container()
        self.setup_center_container()

        self.update_fields(self.subcommand_selector.currentText())

        layout.addWidget(self.top_container)
        layout.addWidget(self.name_container)
        layout.addWidget(self.description_container)
        layout.addStretch()
        layout.addLayout(self.buttons_layout())

    def update_fields(self, command: str):
        if command == "create":
            self.name_container.show()
            self.description_container.show()
        elif command == "restore":
            self.name_container.show()
            self.description_container.hide()
        elif command == "list":
            self.name_container.hide()
            self.description_container.hide()

    def execute(self):
        subcommand = self.subcommand_selector.currentText()

        name = ''
        if subcommand in ["create", "restore"]:
            name = self.name_input.text().strip()
            if not name:
                QtWidgets.QMessageBox.warning(self, "Missing Name", "Please provide snapshot name.")
                return

        if subcommand == "create":
            description = self.description_input.text().strip()
            self.use_case = self.use_cases.create_snapshot_use_case()
            self.dto = CreateSnapshotUseCaseDTO(name, description)

        if subcommand == "restore":
            self.use_case = self.use_cases.restore_snapshot_use_case()
            self.dto = RestoreSnapshotUseCaseDTO(name)

        if subcommand == "list":
            self.use_case = self.use_cases.list_snapshots_use_case()
            self.dto = ListSnapshotsUseCaseDTO()

        def runner():
            self.use_case.execute(self.dto)

        thread = threading.Thread(target=runner)
        thread.start()
        self.accept()

    def setup_top_container(self) -> None:
        self.top_container = QtWidgets.QWidget()
        top_layout = QtWidgets.QVBoxLayout(self.top_container)
        top_layout.setContentsMargins(0,0,0,0)

        snapshot_label = QtWidgets.QLabel("Snapshot action:")
        self.subcommand_selector = QtWidgets.QComboBox()
        self.subcommand_selector.addItems(["create", "list", "restore"])
        self.subcommand_selector.currentTextChanged.connect(self.update_fields)

        top_layout.addWidget(snapshot_label)
        top_layout.addWidget(self.subcommand_selector)

    def setup_center_container(self) -> None:
        self.name_container = QtWidgets.QWidget()
        name_layout = QtWidgets.QVBoxLayout(self.name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_label = QtWidgets.QLabel("Snapshot name:")
        self.name_input = QtWidgets.QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)

        self.description_container = QtWidgets.QWidget()
        description_layout = QtWidgets.QVBoxLayout(self.description_container)
        description_layout.setContentsMargins(0, 0, 0, 0)
        self.description_label = QtWidgets.QLabel("Description (optional):")
        self.description_input = QtWidgets.QLineEdit()
        description_layout.addWidget(self.description_label)
        description_layout.addWidget(self.description_input)