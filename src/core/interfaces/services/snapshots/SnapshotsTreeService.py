from abc import ABC, abstractmethod
from typing import List

from src.core.entities.Snapshot import Snapshot


class SnapshotsTreeService(ABC):
    @abstractmethod
    def get_tree_data(self) -> List[Snapshot]: pass

    @abstractmethod
    def get_flat_list(self) -> List[Snapshot]: pass

    @abstractmethod
    def parse_output(self, text: str) -> None: pass
