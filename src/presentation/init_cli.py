import argparse
import sys

import src
from src.presentation.cli.BaseSubparsers import BaseSubparsers


def init():
    config_path = src.__config_path__

    parser = argparse.ArgumentParser(description="hi")
    subparsers = parser.add_subparsers(dest='', metavar='')

    BaseSubparsers(subparsers=subparsers, config_path=config_path).init()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    args.func(args)