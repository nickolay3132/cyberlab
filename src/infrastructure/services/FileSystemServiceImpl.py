import hashlib
import os
from pathlib import Path
import requests

from src.core.exceptions.CantScanDirectory import CantScanDirectoryError, CantScanDirectory
from src.core.interfaces.output.OutputHandler import OutputHandler
from src.core.interfaces.services.FileSystemService import FileSystemService


class FileSystemServiceImpl(FileSystemService):
    def download_file(self, url: str, download_path: str, output_handler: OutputHandler) -> None:
        temp_file = f"{download_path}.tmp"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192

            with open(temp_file, "wb") as file:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
                    downloaded += block_size
                    output_handler.progress_bar().update(downloaded, total_size)

            os.rename(temp_file, download_path)
            output_handler.progress_bar().close()

        except KeyboardInterrupt as interrupt:
            # (Andrew) TODO: add keyboard interruption handling
            print("Download has been interrupted")
            os.remove(temp_file)

        except Exception as e:
            print(f"\nError fetching url: {url}\n{str(e)}")
            os.remove(temp_file)

    def mkdirs(self, *paths: str):
        for p in paths:
            if not os.path.exists(p):
                os.makedirs(p)

    def to_absolute_path(self, path: str) -> str:
        expanded_path = os.path.expanduser(path)

        if os.path.isabs(expanded_path):
            return os.path.normpath(expanded_path)
        else:
            return os.path.normpath(os.path.join(os.getcwd(), expanded_path))

    def find_files(self, directory: str, *extensions: str) -> list[tuple[str, str]]:
        try:
            dir_path = Path(directory).absolute()
            normalized_exts = {f".{ext.lower().lstrip('.')}" for ext in extensions}

            return [
                (file.stem, str(file))
                for file in dir_path.rglob('*')
                if file.is_file() and file.suffix.lower() in normalized_exts
            ]

        except Exception as e:
            raise CantScanDirectoryError(CantScanDirectory(
                message=f"Error scanning directory: {e}",
                dir_path=directory,
            ))

    def calc_md5(self, file_path: str) -> str:
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()