from src.commands import install, startup


def add_install_parser(subparser):
    install_parser = subparser.add_parser('install', help='Install and import virtual machines')
    install_parser.add_argument(
        '--skip-fetching',
        action='store_true',
        default=False,
        help='skip downloading OVA files (use local copies only)'
    )
    install_parser.set_defaults(func=install.run)

def add_startup_parser(subparser):
    startup_parser = subparser.add_parser('startup', help='Startup all cyberlab virtual machines')
    startup_parser.set_defaults(func=startup.run)