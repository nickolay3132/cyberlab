import argparse
import sys

from src.infrastructure.containers.Commands import Commands
from src.infrastructure.containers.Output import Output
from src.infrastructure.containers.Repos import Repos
from src.infrastructure.containers.Services import Services
from src.infrastructure.containers.UseCases import UseCases
from src.presentation.cli.BaseSubparsers import BaseSubparsers


def init():
    parser = argparse.ArgumentParser(description="hi")
    subparsers = parser.add_subparsers(dest='', metavar='')

    containers = _init_containers()

    BaseSubparsers(subparsers=subparsers, containers=containers).init()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    args.func(args)

def _init_containers():
    repos_container = Repos()
    output_container = Output()
    services_container = Services(repos=repos_container, output=output_container)
    use_cases_container = UseCases(services=services_container)
    base_commands_container = Commands(use_cases=use_cases_container)

    return {
        'repos': repos_container,
        'output': output_container,
        'services': services_container,
        'use_cases': use_cases_container,
        'base_commands': base_commands_container,
    }