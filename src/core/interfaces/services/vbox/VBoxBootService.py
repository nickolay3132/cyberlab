from abc import ABC, abstractmethod


class VBoxBootService(ABC):
    @abstractmethod
    def startup(self) -> None: pass

    @abstractmethod
    def shutdown(self, force: bool = False) -> None: pass