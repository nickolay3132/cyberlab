import sys
from typing import Dict, Tuple, List, Type

from PyQt6.QtWidgets import QApplication

from src.infrastructure.containers.CLIOutput import CLIOutput
from src.infrastructure.containers.Repos import Repos
from src.infrastructure.containers.Services import Services
from src.infrastructure.containers.UseCases import UseCases
from src.presentation.gui.MainWindow import MainWindow
from src.presentation.gui.dialogues.Dialog import Dialog
from src.presentation.gui.dialogues.InstallDialog import InstallDialog
from src.presentation.gui.dialogues.ShutdownDialog import ShutdownDialog
from src.presentation.gui.dialogues.SnapshotDualog import SnapshotDialog
from src.presentation.gui.dialogues.StartupDialog import StartupDialog
from src.presentation.gui.observers.gui_observer_invoker import GUIObserverInvoker
from src.presentation.gui.observers.progressbar_gui_observer import ProgressBarGuiObserver
from src.presentation.gui.observers.texts_gui_observer import TextsGuiObserver


class Main:
    window: MainWindow
    buttons: Dict[str, Tuple[Type[Dialog], List[Type[GUIObserverInvoker]]]] = {
        'install': (InstallDialog, [TextsGuiObserver, ProgressBarGuiObserver]),
        'startup': (StartupDialog, [TextsGuiObserver]),
        'shutdown': (ShutdownDialog, [TextsGuiObserver]),
        'snapshot': (SnapshotDialog, [TextsGuiObserver]),
    }
    containers = {}

    @staticmethod
    def main():
        Main.containers = Main.init_gui_containers()
        app = QApplication(sys.argv)
        Main.window = MainWindow(Main.buttons, Main.button_callback)
        Main.window.show()
        sys.exit(app.exec())

    @staticmethod
    def button_callback(button_label: str) -> None:
        button = Main.buttons[button_label]

        dialog = button[0](
            parent=Main.window,
            use_cases=Main.containers['use_cases'],
            observers=[observer(Main.window.statuses_panel.vm_logs) for observer in button[1]],
        )
        dialog.exec()

    @staticmethod
    def init_gui_containers() -> dict:
        repos_container = Repos()
        output_container = CLIOutput()
        services_container = Services(repos=repos_container, output=output_container)
        use_cases_container = UseCases(services=services_container)

        return {
            "repos": repos_container,
            "output": output_container,
            "services": services_container,
            "use_cases": use_cases_container,
        }

if __name__ == "__main__":
    Main.main()