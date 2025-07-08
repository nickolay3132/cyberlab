from argparse import _SubParsersAction

from src.infrastructure.containers.Commands import Commands
from src.presentation.cli.Subparsers import Subparsers
from src.presentation.commands.BaseCommands import BaseCommands


class BaseSubparsers (Subparsers):
    def __init__(self, subparsers: _SubParsersAction, containers: dict):
        super().__init__(subparsers)
        base_commands_container: Commands = containers.get('base_commands')
        self.base_commands: BaseCommands = base_commands_container.base_commands()

    def add_install_subparser(self):
        parser = self.subparsers.add_parser('install', help='Install and import virtual machines')
        parser.add_argument(
            '--skip-download',
            action='store_true',
            default=False,
            help='skip downloading OVA files'
        )
        parser.add_argument(
            '--no-verify',
            action='store_true',
            default=False,
            help='skip checking OVA file hash if file is already installed'
        )
        parser.set_defaults(func=self.base_commands.install)

    def add_startup_subparser(self):
        parser = self.subparsers.add_parser('startup', help='Startup all cyberlab virtual machines')
        parser.set_defaults(func=self.base_commands.startup)

    def add_shutdown_subparser(self):
        parser = self.subparsers.add_parser('shutdown', help='Shutdown all cyberlab virtual machines')
        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
            help='force shutdown of all cyberlab virtual machines'
        )
        parser.set_defaults(func=self.base_commands.shutdown)