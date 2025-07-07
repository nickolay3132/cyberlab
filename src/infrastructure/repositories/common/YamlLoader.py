from typing import Any

import yaml

from src.core.exceptions.YamlLoaderError import YamlLoaderError, YamlError


class YamlLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Any = None

    def read(self) -> Any:
        if not self.data is None:
            return self.data

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            raise YamlLoaderError(YamlError(
                message="YAML file not found",
                details=str(e),
                file_path=self.file_path
            ))
        except yaml.YAMLError as e:
            raise YamlLoaderError(YamlError(
                message="Invalid YAML syntax",
                details=str(e),
                file_path=self.file_path
            ))




