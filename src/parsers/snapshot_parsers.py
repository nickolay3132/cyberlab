from src.commands.snapshot import create, list_snapshots


def add_create_snapshot_parser(subparser):
    create_parser = subparser.add_parser('create', help='Create snapshot')
    create_parser.add_argument('-n', '--name', required=True, help='snapshot name')
    create_parser.add_argument('-d', '--description', help='helps specify exact state', default="")
    create_parser.add_argument('--vm', help='create snapshot for specific virtual machine', default="")
    create_parser.set_defaults(func=create.run)

def add_list_snapshot_parser(subparser):
    list_parser = subparser.add_parser('list', help='List snapshots')
    list_parser.set_defaults(func=list_snapshots.run)