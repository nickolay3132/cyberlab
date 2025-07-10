from abc import ABC, abstractmethod
from typing import Tuple

from src.core.entities.VirtualMachine import VirtualMachine, Nic


class VBoxNetworksService(ABC):
    @abstractmethod
    def create_nat_net(self) -> bool: pass

    @abstractmethod
    def enable_nat_network(self, vm: VirtualMachine, nic: Nic) -> bool: pass

    @abstractmethod
    def enable_networks(self) -> Tuple[bool]: pass