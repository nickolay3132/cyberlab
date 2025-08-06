import argparse
import sys
from pathlib import Path

import src
from src.bootstrap import get, bootstrap
from src.core.interfaces.repositories import IStorageRepository, IVMRepository
from src.core.interfaces.services import IFileSystemService
from src.core.use_cases import InstallUseCase, InstallUseCaseDto, FetchConfigUseCase
from src.core.use_cases.fetch_config_use_case import FetchConfigUseCaseDto
from src.infrastructure.repositories import YamlLoader


def main():
    parser = argparse.ArgumentParser(description="GUI/CLI приложение")
    parser.add_argument('mode', nargs='?', choices=['cli'], help="Режим запуска: cli или ничего (для GUI)")
    args, _ = parser.parse_known_args()

    if args.mode == 'cli':
        pass
    else:
        pass

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        root_dir = Path(sys.executable).parent
    else:
        root_dir = Path(__file__).resolve().parent

    bootstrap()
    # main()

    # yaml_loader = get(YamlLoader)('./config.yaml')
    # storage_repo = get(IStorageRepository)(yaml_loader)
    # vm_repo = get(IVMRepository)(yaml_loader)
    #
    # install_use_case = get(InstallUseCase)(storage_repo, vm_repo)
    #
    # install_use_case.execute(InstallUseCaseDto(False, False))

    # file_system_service = get(IFileSystemService)()
    # fetch_config_use_case = get(FetchConfigUseCase)(file_system_service)
    #
    # fetch_config_use_case.execute(FetchConfigUseCaseDto(
    #     str(root_dir), src.__version__, src.__repository__
    # ))

    install_use_case = get(InstallUseCase)(f"{root_dir}/config.yaml", '')

    install_use_case.execute(InstallUseCaseDto(
        src.__repository__,
        False,
        False,
    ))