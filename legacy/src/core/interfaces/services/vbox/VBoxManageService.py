from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities.VirtualMachine import VirtualMachine
from src.core.interfaces.services.vbox.VBoxBootService import VBoxBootService
from src.core.interfaces.services.vbox.VBoxImportService import VBoxImportService
from src.core.interfaces.services.vbox.VBoxNetworksService import VBoxNetworksService


class VBoxManageService (ABC):
    @abstractmethod
    def import_vms(self, reimport: Optional[List[VirtualMachine]]) -> None: pass

    @abstractmethod

    @abstractmethod
    def networks(self) -> VBoxNetworksService: pass

    @abstractmethod
    def boot(self) -> VBoxBootService: pass