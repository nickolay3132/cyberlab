import platform
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.presentation.gui.MainWindow import MainWindow
from src.presentation.gui.RunTerminalCommand import RunTerminalCommand
from src.presentation.gui.dialogues.InstallDialog import InstallDialog
from src.presentation.gui.dialogues.ShutdownDialog import ShutdownDialog
from src.presentation.gui.dialogues.SnapshotDualog import SnapshotDialog
from src.presentation.gui.dialogues.StartupDialog import StartupDialog


class Main:
    window: MainWindow
    buttons = {
        'install': InstallDialog,
        'startup': StartupDialog,
        'shutdown': ShutdownDialog,
        'snapshot': SnapshotDialog,
    }
    run_terminal_command = RunTerminalCommand(platform.system())

    @staticmethod
    def main():
        app = QApplication(sys.argv)
        Main.window = MainWindow(Main.buttons, Main.button_callback)
        Main.window.show()
        sys.exit(app.exec())

    @staticmethod
    def button_callback(button_label: str) -> None:
        base_path = Path(__file__).parent

        if sys.platform.startswith("win") and (base_path / "cyberlab_cli.exe").exists():
            cmd = ['cyberlab_cli.exe']
        elif (base_path / "cyberlab_cli").exists():
            cmd = ['cyberlab_cli']
        else:
            cmd = ['python', 'cyberlab_cli.py']

        dialog = Main.buttons.get(button_label)(
            cmd=cmd,
            command_executor=Main.run_terminal_command,
            parent=Main.window,
        )
        dialog.exec()

if __name__ == "__main__":
    Main.main()