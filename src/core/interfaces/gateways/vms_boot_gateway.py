from abc import ABC, abstractmethod


class IVmsBootGateway(ABC):
    @abstractmethod
    def startup(self, vm_name: str, startup_type: str) -> bool: pass

    @abstractmethod
    def shutdown(self, vm_name: str, shutdown_type: str) -> bool: pass
