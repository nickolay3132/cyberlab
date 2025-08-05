from dataclasses import dataclass
from pprint import pprint

from src.core.interfaces.repositories import IStorageRepository, IVMRepository


@dataclass
class InstallUseCaseDto:
    no_verify: bool
    skip_download: bool
    
@dataclass
class InstallUseCase:
    storage_repo: IStorageRepository
    vm_repo: IVMRepository
    
    def execute(self, dto: InstallUseCaseDto):
        storage = self.storage_repo.get()
        vms = self.vm_repo.get_all()
        
        pprint(storage)
        pprint(vms)