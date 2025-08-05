from typing import Any

import yaml


class YamlLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Any = None

    def read(self, create_if_not_exists: bool = False) -> Any:
        if not self.data is None:
            return self.data

        return self._read(create_if_not_exists)

    def write(self, data: Any) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                yaml.safe_dump(data, file,
                               default_flow_style=False,
                               allow_unicode=True,
                               sort_keys=False)

                self.data = yaml.safe_load(file)

        except (IOError, yaml.YAMLError) as e:
            raise yaml.YAMLError(f"Failed to write to {self.file_path}. Message: {e}")

    def _read(self, create_if_not_exists: bool = False) -> Any:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.data = yaml.safe_load(file)
                return self.data
        except FileNotFoundError as e:
            if not create_if_not_exists:
                raise yaml.YAMLError(f"Yaml file {self.file_path} does not exist")

            with open(self.file_path, "w", encoding="utf-8") as _: pass
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid yaml syntax in file {self.file_path}")