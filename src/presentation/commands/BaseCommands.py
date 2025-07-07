from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.use_cases.vm_commands.InstallCommand import InstallCommand
from src.infrastructure.repositories.StorageRepositoryImpl import StorageRepositoryImpl
from src.infrastructure.repositories.VirtualMachinesRepositoryImpl import VirtualMachinesRepositoryImpl
from src.infrastructure.repositories.common.YamlLoader import YamlLoader


class BaseCommands:
    def __init__(self, config_path: str):
        self.yaml_loader = YamlLoader(file_path=config_path)

    def install(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Installing...")

        storage_repository = StorageRepositoryImpl(self.yaml_loader)
        virtual_machines_repository = VirtualMachinesRepositoryImpl(self.yaml_loader)

        InstallCommand(storage_repository, virtual_machines_repository).execute()

    def startup(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Starting up...")

    def shutdown(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Shutting down...")
