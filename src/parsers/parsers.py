import sys

from src.commands import install, startup, shutdown
from src.parsers import snapshot_parsers
from src.texts.BaseTexts import BaseTexts


def add_install_parser(subparser):
    install_parser = subparser.add_parser('install', help='Install and import virtual machines')
    install_parser.add_argument(
        '--skip-download',
        action='store_true',
        default=False,
        help='skip downloading OVA files'
    )
    install_parser.add_argument(
        '--no-verify',
        action='store_true',
        default=False,
        help='skip checking OVA file hash if file is already installed'
    )
    install_parser.set_defaults(func=install.run)

def add_startup_parser(subparser):
    startup_parser = subparser.add_parser('startup', help='Startup all cyberlab virtual machines')
    startup_parser.set_defaults(func=startup.run)

def add_shutdown_parser(subparser):
    shutdown_parser = subparser.add_parser('shutdown', help='Shutdown all cyberlab virtual machines')
    shutdown_parser.add_argument(
        '--force',
        action='store_true',
        default=False,
        help='force shutdown of all cyberlab virtual machines'
    )
    shutdown_parser.set_defaults(func=shutdown.run)

def add_snapshot_parser(subparser):
    description = BaseTexts.snapshots_description()

    snapshot_parser = subparser.add_parser(
        'snapshot',
        help='Manage lab state snapshots',
        description=description)
    snapshot_subparser = snapshot_parser.add_subparsers(dest='snapshot_command', metavar='')

    snapshot_parsers.add_create_snapshot_parser(snapshot_subparser)

    snapshot_parser.set_defaults(func=lambda _: snapshot_parser.print_help() and sys.exit(1))


