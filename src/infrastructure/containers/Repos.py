from dependency_injector import containers, providers

import src
from src.infrastructure.repositories.StorageRepositoryImpl import StorageRepositoryImpl
from src.infrastructure.repositories.VirtualMachinesRepositoryImpl import VirtualMachinesRepositoryImpl
from src.infrastructure.repositories.common.YamlLoader import YamlLoader


class Repos(containers.DeclarativeContainer):
    yaml_loader = providers.Singleton(
        YamlLoader,
        file_path=src.__config_path__
    )

    storage_repository = providers.Factory(
        StorageRepositoryImpl,
        yaml_loader=yaml_loader)

    virtual_machines_repository = providers.Factory(
        VirtualMachinesRepositoryImpl,
        yaml_loader=yaml_loader
    )