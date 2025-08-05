from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from src.core.enums import DownloadingType
from src.core.interfaces.services import IFileSystemService


@dataclass
class FetchConfigUseCaseDto:
    root_dir: str
    version: str
    repository: str

@dataclass
class FetchConfigUseCase:
    file_system_service: IFileSystemService

    def execute(self, dto: FetchConfigUseCaseDto):
        config_name = f"config-{dto.version}.yaml"

        if not self.file_system_service.file_exists(config_name):
            url = urljoin(dto.repository, f"config-{dto.version.replace('.', '')}.yaml")
            res = self.file_system_service.download_file(
                url,
                f"{dto.root_dir}/{config_name}",
                self._progress_handler
            )

            print(f"Finally: {res}")

    @staticmethod
    def _progress_handler(state: DownloadingType, total: int, downloaded: int, error_msg: Optional[str]) -> None:
        print(f"{state.value}: {downloaded}/{total}: {error_msg}")