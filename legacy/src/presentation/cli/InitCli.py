import argparse
import sys
import pyfiglet
from colorama.ansi import Fore
from src import __version__

from src.infrastructure.containers.cli_main_container import CliMainContainer
from src.presentation.cli.subparsers.BaseSubparsers import BaseSubparsers
from src.presentation.cli.subparsers.SnapshotSubparsers import SnapshotSubparsers


class InitCli:
    def __init__(self):
        self.containers = CliMainContainer()

    def run(self):
        parser = argparse.ArgumentParser(description=self._show_cli_header(__version__))
        self._register_subparsers(parser)

        args = parser.parse_args()

        if not hasattr(args, "func"):
            parser.print_help()
            sys.exit(1)

        args.func(args)

    @staticmethod
    def _show_cli_header(version: str):
        ascii_title = pyfiglet.figlet_format("CyberLab CLI", font="slant")
        description = "Cyber Lab management tool".rjust(68)
        version = version.rjust(68)

        header = [
            f"{Fore.BLUE}{ascii_title}",
            f"{Fore.WHITE}{"━" * 68}",
            f"{description}",
            f"{Fore.YELLOW}{version}",
        ]

        print("\n".join(header))

    def _register_subparsers(self, parser: argparse.ArgumentParser):
        subparsers = parser.add_subparsers(dest='', metavar='<command>')

        subparser_classes = (
            BaseSubparsers,
            SnapshotSubparsers,
        )

        for subparser_class in subparser_classes:
            subparser_class(
                subparsers=subparsers,
                commands=self.containers.commands(),
            ).init()