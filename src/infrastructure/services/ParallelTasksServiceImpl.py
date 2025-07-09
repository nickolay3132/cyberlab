import threading
import time
from dataclasses import dataclass
from typing import Callable, Tuple, List, Dict

from src.core.entities.ParrallelTask import ParallelTask, ParallelTaskData
from src.core.interfaces.services.ParallelTasksService import ParallelTasksService



class ParallelTasksServiceImpl(ParallelTasksService):
    def __init__(self):
        self.tasks: List[ParallelTask] = []
        self.lock = threading.Lock()

    def add_task(self, task: Callable[[ParallelTaskData], None], args: Dict) -> None:
        task_data = ParallelTaskData(
            args=args,
            thread_lock=self.lock,
        )
        thread = threading.Thread(
            target=task,
            args=(task_data, ),
            daemon=True,
        )

        with self.lock:
            self.tasks.append(ParallelTask(
                task=task,
                thread=thread,
                data=task_data,
            ))

    def run(self) -> None:
        for task in self.tasks:
            task.thread.start()

    def wait(self, on_complete: Callable[[ParallelTaskData], None]) -> None:
        while True:
            with self.lock:
                if not self.tasks:
                    break
                completed_tasks = [t for t in self.tasks if not t.thread.is_alive()]

                for task in completed_tasks:
                    on_complete(task.data)
                    self.tasks.remove(task)
            time.sleep(0.5)