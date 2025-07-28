from datetime import datetime

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTreeWidgetItem, QPushButton, QTreeWidget, QVBoxLayout, QDialog, QLabel

from src.core.entities.Snapshot import Snapshot


class SnapshotsTreeDialogWidget(QDialog):
    def __init__(self, root_snapshot: Snapshot, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Snapshots Tree")
        self.resize(400, 500)

        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Snapshot Name"])
        layout.addWidget(self.tree)

        self._populate_tree(root_snapshot)
        self.tree.expandAll()

        hint_label = QLabel("Hover over an item to see more details")
        hint_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(hint_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.setModal(True)

    def _populate_tree(self, snapshot: Snapshot, parent_item=None):
        text = snapshot.name
        item = QTreeWidgetItem([text])

        if snapshot.is_current:
            item.setForeground(0, QColor("green"))
            item.setText(0, item.text(0) + " ← current snapshot")

        tooltip_text = (f"Name: {snapshot.name}\n"
                        f"Description: {snapshot.description}\n"
                        f"Date: {datetime.fromtimestamp(snapshot.timestamp)}")
        if snapshot.is_current:
            tooltip_text += "\nThis is the current snapshot"
        item.setToolTip(0, tooltip_text)

        if parent_item:
            parent_item.addChild(item)
        else:
            self.tree.addTopLevelItem(item)

        for child in snapshot.children:
            self._populate_tree(child, item)