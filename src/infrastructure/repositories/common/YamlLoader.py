from typing import Any

import yaml

from src.core.exceptions.YamlLoaderError import YamlLoaderError, YamlError


class YamlLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Any = None

    def read(self, create_if_not_exists: bool = False) -> Any:
        if not self.data is None:
            return self.data

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.data = yaml.safe_load(file)
                return self.data
        except FileNotFoundError as e:
            if not create_if_not_exists:
                raise YamlLoaderError(YamlError(
                    message="YAML file not found",
                    details=str(e),
                    file_path=self.file_path
                ))

            with open(self.file_path, "w", encoding="utf-8") as _: pass
        except yaml.YAMLError as e:
            raise YamlLoaderError(YamlError(
                message="Invalid YAML syntax",
                details=str(e),
                file_path=self.file_path
            ))
    def write(self, data: Any) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file,
                               default_flow_style=False,
                               allow_unicode=True,
                               sort_keys=False)

        except (IOError, yaml.YAMLError) as e:
            raise YamlLoaderError(YamlError(
                message="Failed to write YAML file",
                details=str(e),
                file_path=self.file_path
            ))



