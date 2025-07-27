from abc import abstractmethod
from typing import Self

from src.core.entities.Snapshot import Snapshot
from src.core.entities.event_bus import EventBuilder
from src.core.entities.event_bus.events import SnapshotsTreeEvent


class SnapshotsTreeEventBuilder(EventBuilder):
    @abstractmethod
    def set_root_snapshot(self, snapshot: Snapshot) -> Self: pass

    @abstractmethod
    def build(self) -> SnapshotsTreeEvent: pass