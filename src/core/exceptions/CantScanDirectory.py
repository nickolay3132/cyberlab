from dataclasses import dataclass
from typing import Optional


@dataclass
class CantScanDirectory:
    message: str
    dir_path: Optional[str] = None

class CantScanDirectoryError(Exception):
    def __init__(self, error: CantScanDirectory):
        self.error = error
        super().__init__(error.message)