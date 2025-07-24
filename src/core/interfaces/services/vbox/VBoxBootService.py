from abc import ABC, abstractmethod

from src.core.entities.observer import Subject


class VBoxBootService(ABC):
    @abstractmethod
    def startup(self, subject: Subject) -> None: pass

    @abstractmethod
    def shutdown(self, subject: Subject, force: bool = False) -> None: pass