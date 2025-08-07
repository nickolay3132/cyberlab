from pprint import pprint

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from src.core.entities.event_bus.events import TextEvent


class StartupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = {}

        layout = QVBoxLayout()
        for vm_name in ['firewall-1', 'php-server']:
            label = QLabel(f"{vm_name}: Testing")
            self.labels[vm_name] = label
            layout.addWidget(label)

        self.setLayout(layout)

    def text_event_listener(self, event: TextEvent) -> None:
        pprint(event)
        self.labels[event.id].setText(event.text)