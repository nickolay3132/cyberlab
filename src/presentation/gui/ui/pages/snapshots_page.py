from typing import Callable, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTreeWidget, QTreeWidgetItem

from src.bootstrap import global_vars
from src.core.entities import Snapshot
from src.core.entities.event_bus.events import SnapshotsTreeEvent, TextEvent
from src.core.enums.events import TextEventType


class SnapshotsPage(QWidget):
    snapshots_tree_signal = pyqtSignal(SnapshotsTreeEvent)
    text_event_signal = pyqtSignal(TextEvent)

    def __init__(self):
        super().__init__()
        self.font = global_vars.get('font', QFont())
        self.selected_snapshot: Optional[Snapshot] = None
        self._rendered_items: dict[int, QTreeWidgetItem] = {}
        self._current_path_ids: list[int] = []
        # self.selected_item: Optional[QTreeWidgetItem] = None

        self.snapshots_tree_signal.connect(self._snapshots_tree_handler)
        self.text_event_signal.connect(self._text_event_handler)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMouseTracking(True)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.layout.addWidget(self.tree)

        self.message_label: Optional[QLabel] = None

        self.button_row = QHBoxLayout()
        self.back_home_button = QPushButton("Back to Home")
        self.create_button = QPushButton("Create Snapshot")
        self.rollback_button = QPushButton("Restore Snapshot")

        self.back_home_button.setEnabled(False)
        self.create_button.setEnabled(False)
        self.rollback_button.setEnabled(False)

        self.button_row.addWidget(self.back_home_button)
        self.button_row.addWidget(self.create_button)
        self.button_row.addWidget(self.rollback_button)
        self.layout.addLayout(self.button_row)

    def add_back_home_button(self, callback: Callable[[], None]):
        self.back_home_button.setEnabled(True)
        self.back_home_button.clicked.connect(callback)

    def add_create_button(self, callback: Callable[[], None]):
        self.create_button.setEnabled(True)
        self.create_button.clicked.connect(callback)

    def add_rollback_button(self, callback: Callable[[Snapshot], None]):
        def wrapped():
            if self.selected_snapshot:
                callback(self.selected_snapshot)
        self.rollback_button.clicked.connect(wrapped)

    def snapshots_tree_listener(self, event: SnapshotsTreeEvent) -> None:
        self.snapshots_tree_signal.emit(event)

    def text_event_listener(self, event: TextEvent) -> None:
        self.text_event_signal.emit(event)

    def _snapshots_tree_handler(self, event: SnapshotsTreeEvent) -> None:
        self._render_tree(event.root_snapshot)

    def _text_event_handler(self, event: TextEvent) -> None:
        if self.message_label:
            self.layout.removeWidget(self.message_label)
            self.message_label.deleteLater()

        self.message_label = QLabel()
        self.message_label.setFont(self.font)

        color_map = {
            TextEventType.TITLE: "cyan",
            TextEventType.SUCCESS: "green",
            TextEventType.WARNING: "yellow",
            TextEventType.ERROR: "red"
        }
        color = color_map.get(event.type, "white")
        self.message_label.setText(f"<span style='color: {color};'>{event.text}</span>")
        self.layout.insertWidget(1, self.message_label)

    def _render_tree(self, root: Optional[Snapshot]) -> None:
        self.tree.clear()
        self.selected_snapshot = None
        self.rollback_button.setEnabled(False)
        self._rendered_items.clear()

        if not root:
            self.tree.addTopLevelItem(QTreeWidgetItem(["No snapshots avaliable"]))
            return

        self._build_tree_iteratively(root)
        self._current_path_ids = self._find_path_to_current_ids(root)

        # Разворачиваем только путь к текущему снапшоту
        for snapshot_id in self._current_path_ids:
            item = self._rendered_items.get(snapshot_id)
            if item:
                parent = item.parent()
                while parent:
                    parent.setExpanded(True)
                    parent = parent.parent()
                item.setExpanded(True)

    def _build_tree_iteratively(self, root: Snapshot):
        stack = [(root, None)]  # (snapshot, parent_item)

        while stack:
            snapshot, parent_item = stack.pop()
            label = f"✔️ {snapshot.name}" if snapshot.is_current else snapshot.name

            item = QTreeWidgetItem([label])
            item.setToolTip(0, snapshot.description)
            item.setData(0, Qt.ItemDataRole.UserRole, snapshot)

            if snapshot.is_current:
                item.setForeground(0, Qt.GlobalColor.green)

            if parent_item:
                parent_item.addChild(item)
            else:
                self.tree.addTopLevelItem(item)

            self._rendered_items[id(snapshot)] = item

            for child in reversed(snapshot.children):
                stack.append((child, item))

    def _find_path_to_current_ids(self, root: Snapshot) -> list[int]:
        stack = [(root, [])]  # (node, path_so_far)

        while stack:
            node, path = stack.pop()
            new_path = path + [id(node)]
            if node.is_current:
                return new_path
            for child in reversed(node.children):
                stack.append((child, new_path))
        return []

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        # if self.selected_item:
        #     self.selected_item.setBackground(0, Qt.GlobalColor.transparent)
        #     font = self.selected_item.font(0)
        #     font.setBold(False)
        #     self.selected_item.setFont(0, font)
        #
        # item.setBackground(0, Qt.GlobalColor.cyan)
        # font = item.font(0)
        # font.setBold(True)
        # item.setFont(0, font)

        # self.selected_item = item
        self.selected_snapshot = item.data(0, Qt.ItemDataRole.UserRole)
        self.rollback_button.setText(f'Restore snapshot "{self.selected_snapshot.name}"')
        self.rollback_button.setEnabled(True)