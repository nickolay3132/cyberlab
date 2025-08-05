from asyncio import Future
from dataclasses import dataclass
from typing import List

from src.core.entities.event_bus import Event


@dataclass
class SelectOptionEvent(Event):
    id: str
    options: List[str]
    future: Future