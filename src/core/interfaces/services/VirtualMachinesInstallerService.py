from abc import ABC, abstractmethod

from src.core.entities.observer import Subject


class VirtualMachinesInstallerService (ABC):
    @abstractmethod
    def set_subject(self, subject: Subject) -> 'VirtualMachinesInstallerService': pass
    @abstractmethod
    def install(self, no_verify_checksum: bool = False) -> None: pass