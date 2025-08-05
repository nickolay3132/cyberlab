from src.bootstrap.binder import bind
from src.core.interfaces.services import IFileSystemService
from src.infrastructure.services import FileSystemServiceImpl


@bind
def make_file_system_service() -> IFileSystemService:
    return FileSystemServiceImpl()