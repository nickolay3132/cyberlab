import threading
from dataclasses import dataclass
from typing import Callable, List, Dict


@dataclass
class ParallelTaskData:
    args: Dict
    thread_lock: threading.Lock
    error: str = None
    is_completed: bool = False

@dataclass
class ParallelTask:
    task: Callable
    thread: threading.Thread
    data: ParallelTaskData