from abc import ABC, abstractmethod

from src.core.entities.Storage import Storage


class StorageRepository (ABC):
    @abstractmethod
    def get(self) -> Storage: pass