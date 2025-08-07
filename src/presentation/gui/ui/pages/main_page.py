from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = {}

        layout = QVBoxLayout()
        for vm_name in ['vm1', 'vm2']:
            label = QLabel(f"{vm_name}: Testing")
            self.labels[vm_name] = label
            layout.addWidget(label)

        self.setLayout(layout)