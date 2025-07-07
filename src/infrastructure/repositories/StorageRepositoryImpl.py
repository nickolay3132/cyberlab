from src.core.entities.Storage import Storage
from src.core.interfaces.repositories.StorageRepository import StorageRepository
from src.infrastructure.repositories.common.YamlLoader import YamlLoader


class StorageRepositoryImpl(StorageRepository):
    def __init__(self, yaml_loader: YamlLoader):
        self.data = yaml_loader.read().get("storage", {})

    def get(self) -> Storage:
      return Storage(
            repository=self.data.get("repository", ""),
            ova_store_to=self.data.get("ova_store_to", "./ova"),
            vms_store_to=self.data.get("vms_store_to", "./vms"),
            import_log_store_to=self.data.get("import_log_store_to", "./import_log"),
        )