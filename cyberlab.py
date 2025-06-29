import argparse
import sys

from src import parsers
from src.texts.BaseTexts import BaseTexts


def main():
    parser = argparse.ArgumentParser(description=BaseTexts.hello())
    subparsers = parser.add_subparsers(dest='')

    parsers.add_install_parser(subparsers)
    parsers.add_startup_parser(subparsers)
    parsers.add_shutdown_parser(subparsers)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == '__main__':
    main()