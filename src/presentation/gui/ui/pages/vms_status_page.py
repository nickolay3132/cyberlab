from pprint import pprint

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.core.entities.event_bus.events import TextEvent
from src.presentation.gui.ui.panels import VmsStatusPanel


class VmsStatusesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.panel = VmsStatusPanel()
        self.panel.initialize(['firewall-1', 'php-server'])

        layout = QVBoxLayout()
        layout.addWidget(self.panel)

        self.setLayout(layout)


    def text_event_listener(self, event: TextEvent) -> None:
        pprint(event)
        self.panel.update_text(event)