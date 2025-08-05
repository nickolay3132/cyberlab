from dataclasses import dataclass
from typing import List, Literal


@dataclass
class Nic:
    index: int
    type: Literal["natnetwork", "intnetwork"]
    network_name: str

@dataclass
class BootPolicy:
    startup: Literal["gui", "headless", "separate"] = "gui"
    shutdown: Literal["acpipowerbutton", "poweroff", "savestate"] = "acpipowerbutton"

@dataclass
class VirtualMachine:
    name: str
    ova_filename: str
    md5checksum: str
    nics: List[Nic]
    boot_policy: BootPolicy