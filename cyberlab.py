import sys

from PyQt6.QtWidgets import QApplication

from src.infrastructure.containers.CLIOutput import CLIOutput
from src.infrastructure.containers.Repos import Repos
from src.infrastructure.containers.Services import Services
from src.infrastructure.containers.UseCases import UseCases
from src.presentation.gui.MainWindow import MainWindow
from src.presentation.gui.dialogues.InstallDialog import InstallDialog
from src.presentation.gui.dialogues.ShutdownDialog import ShutdownDialog
from src.presentation.gui.dialogues.SnapshotDualog import SnapshotDialog
from src.presentation.gui.dialogues.StartupDialog import StartupDialog
from src.presentation.gui.gui_observer import GUIObserver


class Main:
    window: MainWindow
    buttons = {
        'install': InstallDialog,
        'startup': StartupDialog,
        'shutdown': ShutdownDialog,
        'snapshot': SnapshotDialog,
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
        dialog = Main.buttons.get(button_label)(
            parent=Main.window,
            use_cases=Main.containers['use_cases'],
            observer=GUIObserver(Main.window.statuses_panel.vm_logs)
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