from src.bootstrap.binder import bind
from src.core.interfaces.repositories import ISnapshotsRepository, IStorageRepository, IVMRepository
from src.infrastructure.repositories import YamlLoader, YamlSnapshotRepository, YamlStorageRepository, YamlVmRepository


@bind
def make_yaml_loader(file_path: str) -> YamlLoader:
    return YamlLoader(file_path)

@bind
def make_snapshots_repo(yaml_loader: YamlLoader) -> ISnapshotsRepository:
    return YamlSnapshotRepository(yaml_loader)

@bind
def make_storage_repo(yaml_loader: YamlLoader) -> IStorageRepository:
    return YamlStorageRepository(yaml_loader)

@bind
def make_vm_repo(yaml_loader: YamlLoader) -> IVMRepository:
    return YamlVmRepository(yaml_loader)