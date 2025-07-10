from abc import ABC, abstractmethod

from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService
from src.core.interfaces.services.vbox.VBoxNetworksService import VBoxNetworksService


class VBoxManageService (ABC):
    @abstractmethod
    def import_vms(self) -> None: pass

    @abstractmethod
    def enable_networks(self) -> None: pass

    @abstractmethod
    def networks(self) -> VBoxNetworksService: pass

    @abstractmethod
    def boot(self) -> VBoxBootService: pass