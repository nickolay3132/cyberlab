from abc import ABC, abstractmethod


class VirtualMachinesInstallerService (ABC):
    @abstractmethod
    def install(self) -> None: pass