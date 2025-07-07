from dataclasses import dataclass
from typing import Optional


@dataclass
class VirtualMachineNotFound:
    message: str
    vm_name: str
    details: Optional[str] = None

class VirtualMachineNotFoundError(Exception):
    def __init__(self, error: VirtualMachineNotFound):
        self.error = error
        super().__init__(error.message)
