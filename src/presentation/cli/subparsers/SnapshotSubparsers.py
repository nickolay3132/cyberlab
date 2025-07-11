import sys
from argparse import _SubParsersAction

from colorama.ansi import Fore, Style

from src.infrastructure.containers.Commands import Commands
from src.presentation.cli.subparsers.Subparsers import Subparsers
from src.presentation.cli.commands.SnapshotCommands import SnapshotCommands


class SnapshotSubparsers(Subparsers):
    def __init__(self, subparsers: _SubParsersAction, commands: Commands):
        self.snapshot_commands: SnapshotCommands = commands.snapshot_commands()

        parser_description = f"{Fore.GREEN}Snapshots preserve the entire state (disk, memory, settings) for easy rollback.{Style.RESET_ALL}"
        parser = subparsers.add_parser('snapshot', help='Manage lab state snapshots', description=parser_description)
        parser.set_defaults(func=lambda _: parser.print_help() and sys.exit(1))

        self.subparsers = parser.add_subparsers(dest='snapshot_command', metavar='<command>')

    def add_create_subparser(self):
        parser = self.subparsers.add_parser('create', help='Save current state of all VMs')
        parser.add_argument('-n', '--name', required=True, help='snapshot name (non-unique allowed)')
        parser.add_argument('-d', '--description', help='contextual details', default="")
        # create_parser.add_argument('--vm', help='create snapshot for specific virtual machine', default="")
        parser.set_defaults(func=self.snapshot_commands.create)

    def add_list_subparser(self):
        parser = self.subparsers.add_parser('list', help='Display all available snapshots with their metadata')
        parser.set_defaults(func=self.snapshot_commands.list)

    def add_restore_subparser(self):
        parser = self.subparsers.add_parser('restore', help='Roll back all VMs to a previously saved state')
        parser.add_argument('-n', '--name', required=True, help='snapshot name')
        parser.set_defaults(func=self.snapshot_commands.restore)

    def add_delete_subparser(self):
        parser = self.subparsers.add_parser('delete', help='Delete snapshot',
                                             description=f'{Fore.RED}Warning:{Style.RESET_ALL} Deleting a Snapshot Will Remove All Its Child Snapshots')
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help='delete all snapshots for CyberLab')
        parser.add_argument('-n', '--name', help='snapshot name')
        parser.set_defaults(func=self.snapshot_commands.delete)