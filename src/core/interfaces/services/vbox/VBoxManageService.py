from abc import ABC, abstractmethod

from src.core.entities.observer import Subject
from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService
from src.core.interfaces.services.vbox.VBoxImportService import VBoxImportService
from src.core.interfaces.services.vbox.VBoxNetworksService import VBoxNetworksService


class VBoxManageService (ABC):
    @abstractmethod
    def import_vms(self, subject: Subject) -> None: pass

    @abstractmethod

    @abstractmethod
    def networks(self) -> VBoxNetworksService: pass

    @abstractmethod
    def boot(self) -> VBoxBootService: pass