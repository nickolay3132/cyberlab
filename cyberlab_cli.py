import sys
from typing import io

import colorama

from src.core.exceptions.VirtualMachineNotFound import VirtualMachineNotFoundError
from src.core.exceptions.YamlLoaderError import YamlLoaderError
from src.presentation.cli.InitCli import InitCli


def main():
    colorama.init(autoreset=True)
    cli = InitCli()

    try:
        cli.run()
    except YamlLoaderError as e:
        cli.output.show_error(f"{e.error.message} in {e.error.file_path}", terminate=True)
    except VirtualMachineNotFoundError as e:
        cli.output.show_error(f"{e.error.message} ({e.error.vm_name})", terminate=True)

if __name__ == "__main__":
    main()