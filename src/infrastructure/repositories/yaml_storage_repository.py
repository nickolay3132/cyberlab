from src.core.entities import Storage
from src.core.interfaces.repositories import IStorageRepository
from src.infrastructure.repositories import YamlLoader


class YamlStorageRepository(IStorageRepository):
    def __init__(self, yaml_loader: YamlLoader):
        self.data = yaml_loader.read().get("storage", {})

    def get(self) -> Storage:
      return Storage(
            ova_store_to=self.data.get("ova_store_to", "./ova"),
            vms_store_to=self.data.get("vms_store_to", "./vms"),
            import_log_store_to=self.data.get("import_log_store_to", "./import_log"),
        )