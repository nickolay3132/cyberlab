import hashlib
import os
import sys

import requests
from datetime import datetime, timedelta
from typing import Callable, Optional

from src.core.enums import DownloadingType
from src.core.interfaces.services import IFileSystemService


class FileSystemServiceImpl(IFileSystemService):
    def download_file(self,
                      url: str,
                      download_path: str,
                      callback: Callable[[DownloadingType, int, int, Optional[str]], None]
                      ) -> bool:
        temp_file = f"{download_path}.temp"

        notify_interval = timedelta(seconds=0.5)

        try:
            self._fetch_url(url, temp_file, notify_interval, callback)

            if os.path.exists(download_path):
                os.remove(download_path)
            os.rename(temp_file, download_path)

            callback(DownloadingType.COMPLETED, 0, 0, None)
            return True

        except KeyboardInterrupt as _:
            callback(DownloadingType.FAILED, 0, 0, "Download interrupted")
            sys.exit(1)

        except Exception or ConnectionError as e:
            callback(DownloadingType.FAILED, 0, 0, f"Cannot fetch {url}, Message: {e}")
            return False


    def mkdirs(self, *paths: str) -> None:
        for p in paths:
            if not os.path.exists(p):
                os.makedirs(p)

    def file_exists(self, path: str) -> bool:
        return os.path.exists(path)


    def to_absolute_path(self, path: str) -> str:
        expanded_path = os.path.expanduser(path)

        if os.path.isabs(expanded_path):
            return os.path.normpath(expanded_path)
        else:
            return os.path.normpath(os.path.join(os.getcwd(), expanded_path))

    def calc_md5(self, file_path: str) -> str:
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    @staticmethod
    def _fetch_url(url: str,
                   temp_file: str,
                   notify_interval: timedelta,
                   callback: Callable[[DownloadingType, int, int, Optional[str]], None]
                   ):
        last_notify_time = datetime.now()

        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        block_size = 8192

        with open(temp_file, "wb") as file:
            downloaded = 0
            callback(DownloadingType.INIT, total_size, downloaded, None)

            for chunk in response.iter_content(chunk_size=block_size):
                file.write(chunk)
                downloaded += block_size

                current_time = datetime.now()
                if current_time - last_notify_time >= notify_interval:
                    callback(DownloadingType.IN_PROGRESS, total_size, downloaded, None)
                    last_notify_time = current_time