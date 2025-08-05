from abc import ABC, abstractmethod

from src.core.entities import Storage


class IStorageRepository(ABC):
    @abstractmethod
    def get(self) -> Storage: pass