import threading
from dataclasses import dataclass
from typing import Dict


@dataclass
class ParallelTask:
    args: Dict
    thread_lock: threading.Lock
    error: str = None
    is_completed: bool = False