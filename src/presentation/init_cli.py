import argparse
import sys

import pyfiglet
from colorama.ansi import Fore, Style
import colorama
from src import __version__

from src.core.exceptions.VirtualMachineNotFound import VirtualMachineNotFoundError
from src.core.exceptions.YamlLoaderError import YamlLoaderError
from src.infrastructure.containers.Commands import Commands
from src.infrastructure.containers.Output import Output
from src.infrastructure.containers.Repos import Repos
from src.infrastructure.containers.Services import Services
from src.infrastructure.containers.UseCases import UseCases
from src.presentation.cli.BaseSubparsers import BaseSubparsers
from src.presentation.cli.SnapshotSubparsers import SnapshotSubparsers


def init():
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser(description=cli_hello())
    subparsers = parser.add_subparsers(dest='', metavar='[COMMAND]')

    containers = _init_containers()
    output = containers.get('output').cli_output_handler()

    try:
        _import_subparsers(subparsers, containers.get('commands'))

        args = parser.parse_args()

        if not hasattr(args, 'func'):
            parser.print_help()
            sys.exit(1)

        args.func(args)
    except YamlLoaderError as e:
        output.show_error(f"{e.error.message} in {e.error.file_path}", terminate=True)
    except VirtualMachineNotFoundError as e:
        output.show_error(f"{e.error.message} ({e.error.vm_name})", terminate=True)

def cli_hello():
    ascii_title = pyfiglet.figlet_format("CyberLab CLI", font="slant")
    description = "Cyber Lab management tool".rjust(68)
    version = __version__.rjust(68)

    header = [
        f"{Fore.BLUE}{ascii_title}",
        f"{Fore.WHITE}{"━" * 68}",
        f"{description}",
        f"{Fore.YELLOW}{version}",
    ]

    print("\n".join(header))

def _init_containers():
    repos_container = Repos()
    output_container = Output()
    services_container = Services(repos=repos_container, output=output_container)
    use_cases_container = UseCases(services=services_container, output=output_container)
    commands_container = Commands(use_cases=use_cases_container)

    return {
        'repos': repos_container,
        'output': output_container,
        'services': services_container,
        'use_cases': use_cases_container,
        'commands': commands_container,
    }

def _import_subparsers(subparsers, commands):
    subparsers_classes = (
        BaseSubparsers,
        SnapshotSubparsers,
    )

    for subparser_class in subparsers_classes:
        subparser_class(subparsers=subparsers, commands=commands).init()