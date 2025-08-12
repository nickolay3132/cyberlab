from src.presentation.cli.handlers import (
    handle_install,
    handle_startup,
    handle_shutdown,
    handle_snapshot_create,
    handle_snapshot_list,
    handle_snapshot_restore,
)


def register_install_command(subparsers):
    install_parser = subparsers.add_parser("install", help="install virtual machines")
    install_parser.add_argument("--skip-download", action="store_true", help="skip downloading ova-files")
    install_parser.add_argument("--no-verify", action="store_true", help="skip ova-files verification step")
    install_parser.set_defaults(func=handle_install)

def register_startup_command(subparsers):
    startup_parser = subparsers.add_parser("startup", help="start VMs")
    startup_parser.set_defaults(func=handle_startup)

def register_shutdown_command(subparsers):
    shutdown_parser = subparsers.add_parser("shutdown", help="shutdown VMs")
    shutdown_parser.add_argument("--force", action='store_true', help="force Shutdown")
    shutdown_parser.set_defaults(func=handle_shutdown)

def register_snapshot_commands(subparsers):
    snapshot_parser = subparsers.add_parser("snapshot", help="snapshot operations")
    snapshot_subparsers = snapshot_parser.add_subparsers(dest="snapshot_cmd")

    # create
    create_parser = snapshot_subparsers.add_parser("create", help="create a snapshot")
    create_parser.add_argument("-n", "--name", required=True, help="snapshot name")
    create_parser.add_argument("-d", "--description", help="snapshot description")
    create_parser.set_defaults(func=handle_snapshot_create)

    # list
    list_parser = snapshot_subparsers.add_parser("list", help="list snapshots")
    list_parser.set_defaults(func=handle_snapshot_list)

    # restore
    restore_parser = snapshot_subparsers.add_parser("restore", help="restore snapshot")
    restore_parser.add_argument("-n", "--name", required=True, help="snapshot name to restore")
    restore_parser.set_defaults(func=handle_snapshot_restore)

    # print help by default
    snapshot_parser.set_defaults(func=lambda args: snapshot_parser.print_help())