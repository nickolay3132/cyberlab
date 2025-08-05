from src.bootstrap.binder import bind
from src.core.interfaces.repositories import IStorageRepository, IVMRepository
from src.core.interfaces.services import IFileSystemService
from src.core.use_cases import InstallUseCase, FetchConfigUseCase


@bind
def make_fetch_config_use_case(file_system_service: IFileSystemService) -> FetchConfigUseCase:
    return FetchConfigUseCase(file_system_service)

@bind
def make_install_use_case(
        storage_repo: IStorageRepository,
        vm_repo: IVMRepository,
) -> InstallUseCase:
    return InstallUseCase(storage_repo, vm_repo)