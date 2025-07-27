from abc import ABC, abstractmethod
from asyncio import Future
from dataclasses import dataclass
from typing import Any, List

from src.core.entities.Snapshot import Snapshot
from src.core.entities.progress_bar_data import ProgressBarData


@dataclass
class ObserverEvent:
    id: str
    type: str
    data: Any

    @classmethod
    def title(cls, id: str, data: str) -> 'ObserverEvent':
        return cls(id, 'title', data)

    @classmethod
    def text(cls, id: str, data: str) -> 'ObserverEvent':
        return cls(id, 'text', data)

    @classmethod
    def success(cls, id: str, data: str) -> 'ObserverEvent':
        return cls(id, 'success', data)

    @classmethod
    def warning(cls, id: str, data: str) -> 'ObserverEvent':
        return cls(id, 'warning', data)

    @classmethod
    def error(cls, id: str, data: str) -> 'ObserverEvent':
        return cls(id, 'error', data)

    @classmethod
    def progress(cls, id: str, data: ProgressBarData) -> 'ObserverEvent':
        return cls(id, 'progress', data)

    @classmethod
    def space(cls, id: str) -> 'ObserverEvent':
        return cls(id, 'space', None)

    @classmethod
    def select_option(cls, id: str, options: List[str], future: Future) -> 'ObserverEvent':
        return cls(id, 'select_option', {'options': options, 'future': future})

    @classmethod
    def display_snapshot_tree(cls, root_snapshot: Snapshot) -> 'ObserverEvent':
        return cls('dialog', 'display_snapshot_tree', root_snapshot)

class Observer(ABC):
    @abstractmethod
    def update(self, data: ObserverEvent) -> None: pass

    @abstractmethod
    def on_detach(self) -> None: pass

class Subject:
    def __init__(self) -> None:
        self.observers = []
        
    def attach(self, observer: Observer) -> None: 
        self.observers.append(observer)
        
    def detach(self, observer: Observer) -> None:
        try:
            observer.on_detach()
        finally:
            if observer in self.observers:
                self.observers.remove(observer)

    def notify(self, data: ObserverEvent) -> None:
        for observer in self.observers:
            observer.update(data)