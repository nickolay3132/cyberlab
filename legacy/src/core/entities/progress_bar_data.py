from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ProgressBarStates(Enum):
    INIT = 'init'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    ERROR = 'error'

@dataclass
class ProgressBarData:
    state: ProgressBarStates
    total: int = 0
    actual: int = 0
    error_msg: Optional[str] = None
