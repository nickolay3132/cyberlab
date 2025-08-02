from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import os
import sys
from pathlib import Path

import requests

from src.core.entities.event_bus import EventBus
from src.core.entities.event_bus.events import ProgressEvent, ProgressEventStates
from src.core.exceptions.CantScanDirectory import CantScanDirectoryError, CantScanDirectory
from src.core.interfaces.services.FileSystemService import FileSystemService

@dataclass
class FileSystemServiceImpl(FileSystemService):
    progress_event_bus: EventBus[ProgressEvent]

    def download_file(self, url: str, download_path: str, download_id: str) -> None:
        temp_file = f"{download_path}.tmp"

        pb_event = ProgressEvent(
            id=download_id,
            type=ProgressEventStates.INIT
        )

        last_notify_time = datetime.now()
        notify_interval = timedelta(seconds=0.5)

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192

            pb_event.total = total_size
            self.progress_event_bus.notify(pb_event)

            with open(temp_file, "wb") as file:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=block_size):
                    file.write(chunk)
                    downloaded += block_size

                    current_time = datetime.now()
                    if current_time - last_notify_time >= notify_interval:
                        pb_event.type = ProgressEventStates.IN_PROGRESS
                        pb_event.actual = downloaded
                        self.progress_event_bus.notify(pb_event)

                        last_notify_time = current_time

            if os.path.exists(download_path):
                os.remove(download_path)
            os.rename(temp_file, download_path)

            pb_event.type = ProgressEventStates.COMPLETED
            self.progress_event_bus.notify(pb_event)

        except KeyboardInterrupt as _:
            pb_event.type = ProgressEventStates.ERROR
            pb_event.error_message = f"Download interrupted."
            self.progress_event_bus.notify(pb_event)

            os.remove(temp_file)
            sys.exit(1)

        except Exception or ConnectionError as e:
            pb_event.type = ProgressEventStates.ERROR
            pb_event.error_message = f"Cannot fetch url: {url}, Message: {str(e)}"
            self.progress_event_bus.notify(pb_event)
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
                message=f"Cannot scanning directory: {e}",
                dir_path=directory,
            ))

    def calc_md5(self, file_path: str) -> str:
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()