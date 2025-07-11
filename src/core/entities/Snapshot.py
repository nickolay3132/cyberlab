from dataclasses import dataclass
from typing import List


@dataclass
class Snapshot:
    name: str
    description: str
    timestamp: int
    is_current: bool
    children: List['Snapshot']