from dataclasses import dataclass
from typing import List

from src.core.enums import NicType, BootPolicyStartupType, BootPolicyShutdownType


@dataclass
class Nic:
    index: int
    type: NicType
    network_name: str

@dataclass
class BootPolicy:
    startup: BootPolicyStartupType
    shutdown: BootPolicyShutdownType

@dataclass
class VM:
    name: str
    ova_filename: str
    md5checksum: str
    nics: List[Nic]
    boot_policy: BootPolicy