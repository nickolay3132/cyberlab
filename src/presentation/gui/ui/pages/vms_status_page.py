from pprint import pprint

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.core.entities.event_bus.events import TextEvent, VmsListEvent
from src.presentation.gui.ui.panels import VmsStatusPanel


class VmsStatusesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.panel = VmsStatusPanel()

        layout = QVBoxLayout()
        layout.addWidget(self.panel)

        self.setLayout(layout)

    def vms_list_event_listener(self, event: VmsListEvent) -> None:
        pprint(event)
        self.panel.render_rows(event.vms_names)

    def text_event_listener(self, event: TextEvent) -> None:
        pprint(event)
        self.panel.update_text(event)