import argparse
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

import src
from src.bootstrap import get, bootstrap, global_vars
from src.core.interfaces.repositories import IStorageRepository, IVMRepository
from src.core.interfaces.services import IFileSystemService
from src.core.use_cases import InstallUseCase, InstallUseCaseDto, FetchConfigUseCase, StartupUseCase, StartupUseCaseDto
from src.core.use_cases.fetch_config_use_case import FetchConfigUseCaseDto
from src.core.use_cases.shutdown_use_case import ShutdownUseCase, ShutdownUseCaseDto
from src.infrastructure.repositories import YamlLoader
from src.presentation.gui.ui import MainWindow


def main():
    # parser = argparse.ArgumentParser(description="GUI/CLI приложение")
    # parser.add_argument('mode', nargs='?', choices=['cli'], help="Режим запуска: cli или ничего (для GUI)")
    # args, _ = parser.parse_known_args()

    if 'cli' in sys.argv:
        print('CLI mode')
        print(sys.argv)
    else:
        app = QApplication([])
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        global_vars['root_dir'] = Path(sys.executable).parent
    else:
        global_vars['root_dir'] = Path(__file__).resolve().parent

    bootstrap()
    main()

    # install_use_case = get(InstallUseCase)(f"{root_dir}/config.yaml", '')
    #
    # install_use_case.execute(InstallUseCaseDto(
    #     src.__repository__,
    #     False,
    #     False,
    # ))

    # startup_use_case = get(StartupUseCase)(f"{global_vars['root_dir']}/config.yaml")
    #
    # startup_use_case.execute(StartupUseCaseDto())

    # shutdown_use_case = get(ShutdownUseCase)(f"{root_dir}/config.yaml")
    #
    # shutdown_use_case.execute(ShutdownUseCaseDto(True))