from dataclasses import dataclass
from typing import Optional


@dataclass
class YamlError:
    message: str
    details: Optional[str] = None
    file_path: Optional[str] = None

class YamlLoaderError(Exception):
    def __init__(self, error: YamlError):
        self.error = error
        super().__init__(error.message)