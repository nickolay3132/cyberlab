from abc import ABC, abstractmethod


class VirtualMachinesInstallerService (ABC):
    @abstractmethod
    def install(self, no_verify_checksum: bool = False) -> None: pass