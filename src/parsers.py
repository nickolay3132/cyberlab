from src.commands import install


def add_install_parser(subparser):
    install_parser = subparser.add_parser('install', help='Install and import virtual machines')
    install_parser.add_argument(
        '--skip-fetching',
        action='store_true',
        default=False,
        help='Skip downloading OVA files (use local copies only)'
    )
    install_parser.set_defaults(func=install.run)