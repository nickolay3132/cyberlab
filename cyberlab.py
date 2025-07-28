import sys
from typing import Dict, Type

from PyQt6.QtWidgets import QApplication

from src.infrastructure.containers.gui_main_container import GuiMainContainer
from src.presentation.gui.MainWindow import MainWindow
from src.presentation.gui.dialogues.Dialog import Dialog
from src.presentation.gui.dialogues.InstallDialog import InstallDialog
from src.presentation.gui.dialogues.ShutdownDialog import ShutdownDialog
from src.presentation.gui.dialogues.SnapshotDualog import SnapshotDialog
from src.presentation.gui.dialogues.StartupDialog import StartupDialog

class Main:
    window: MainWindow
    buttons: Dict[str, Type[Dialog]] = {
        'install': InstallDialog,
        'startup': StartupDialog,
        'shutdown': ShutdownDialog,
        'snapshot': SnapshotDialog,
    }
    containers: GuiMainContainer = GuiMainContainer()

    @staticmethod
    def main():
        app = QApplication(sys.argv)
        Main.window = MainWindow(Main.buttons, Main.button_callback)
        Main.containers.layout_map.from_dict(Main.window.statuses_panel.vm_logs)
        Main.window.show()
        sys.exit(app.exec())

    @staticmethod
    def button_callback(button_label: str) -> None:
        handler = Main.buttons[button_label]

        dialog = handler(
            parent=Main.window,
            use_cases=Main.containers.use_cases.provided(),
        )
        dialog.exec()

if __name__ == "__main__":
    Main.main()