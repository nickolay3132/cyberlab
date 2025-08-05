from abc import ABC, abstractmethod



class FileSystemService(ABC):
    @abstractmethod
    def download_file(self, url: str, download_path: str, download_id: str) -> None: pass

    @abstractmethod
    def mkdirs(self, *paths: str): pass

    @abstractmethod
    def to_absolute_path(self, path: str) -> str: pass

    @abstractmethod
    def find_files(self, directory: str, *extensions: str) -> list[tuple[str, str]]: pass

    @abstractmethod
    def calc_md5(self, file_path: str) -> str: pass