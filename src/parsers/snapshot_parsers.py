from colorama.ansi import Fore, Style

from src.commands.snapshot import create, list_snapshots, restore, delete


def add_create_snapshot_parser(subparser):
    create_parser = subparser.add_parser('create', help='Save current state of all VMs')
    create_parser.add_argument('-n', '--name', required=True, help='snapshot name (non-unique allowed)')
    create_parser.add_argument('-d', '--description', help='contextual details', default="")
    # create_parser.add_argument('--vm', help='create snapshot for specific virtual machine', default="")
    create_parser.set_defaults(func=create.run)

def add_list_snapshot_parser(subparser):
    list_parser = subparser.add_parser('list', help='Display all available snapshots with their metadata')
    list_parser.set_defaults(func=list_snapshots.run)

def add_restore_snapshot_parser(subparser):
    restore_parser = subparser.add_parser('restore', help='Roll back all VMs to a previously saved state')
    restore_parser.add_argument('-n', '--name', required=True, help='snapshot name')
    restore_parser.set_defaults(func=restore.run)

def add_delete_snapshot_parser(subparser):
    delete_parser = subparser.add_parser('delete', help='Delete snapshot',
                                         description=f'{Fore.RED}Warning:{Style.RESET_ALL} Deleting a Snapshot Will Remove All Its Child Snapshots')
    delete_parser.add_argument(
        '--all',
        action='store_true',
        default=False,
        help='delete all snapshots for CyberLab')
    delete_parser.add_argument('-n', '--name', help='snapshot name')
    delete_parser.set_defaults(func=delete.run)