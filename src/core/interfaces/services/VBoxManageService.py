from abc import ABC, abstractmethod


class VBoxManageService (ABC):
    @abstractmethod
    def import_vms(self) -> None: pass