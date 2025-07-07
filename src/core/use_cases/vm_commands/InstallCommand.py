from pprint import pprint

from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.core.interfaces.repositories.VirtualMachinesRepository import VirtualMachinesRepository


class InstallCommand:
    def __init__(
            self,
            storage_repository: StorageRepository,
            virtual_machines_repository: VirtualMachinesRepository
    ):
        self.storage_repository = storage_repository
        self.virtual_machines_repository = virtual_machines_repository

    def execute(self):
        print(f"ova_store_to: {self.storage_repository.get().ova_store_to}")
        pprint(self.virtual_machines_repository.get_all())