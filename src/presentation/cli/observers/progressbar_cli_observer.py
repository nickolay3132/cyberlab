from typing import cast, Dict, Callable

from colorama.ansi import Fore, Style
from tqdm import tqdm

from src.core.entities.observer import ObserverEvent
from src.core.entities.progress_bar_data import ProgressBarData, ProgressBarStates
from src.presentation.cli.observers.cli_observer_invoker import CLIObserverInvoker


class ProgressBarCLIObserver(CLIObserverInvoker):
    def __init__(self):
        super().__init__()

        self.pbar = None
        self.add_event_handlers({
            'progress': self.progress_bar_event,
        })

    def progress_bar_event(self, event: ObserverEvent):
        pb_data = cast(ProgressBarData, event.data)

        states_handlers: Dict[ProgressBarStates, Callable[[str, ProgressBarData], None]] = {
            ProgressBarStates.INIT: self.progress_bar_init_event,
            ProgressBarStates.IN_PROGRESS: self.progress_bar_in_progress_event,
            ProgressBarStates.COMPLETED: self.progress_bar_completed_event,
            ProgressBarStates.ERROR: self.progress_bar_error_event,
        }

        handler = states_handlers.get(pb_data.state)
        handler(event.id, pb_data)

    def progress_bar_init_event(self, item_id: str, pb_data: ProgressBarData):
        print(f"Downloading {item_id}...")
        self.pbar = tqdm(total=pb_data.total, unit="B", unit_scale=True, ncols=100)

    def progress_bar_in_progress_event(self, _, pb_data: ProgressBarData):
        self.pbar.update(pb_data.actual - self.pbar.n)

    def progress_bar_completed_event(self, _, __):
        self.pbar.close()
        print()

    def progress_bar_error_event(self, _, pb_data: ProgressBarData):
        self.pbar.close()
        print(f"{Fore.RED}Error: {Style.RESET_ALL}{pb_data.error_msg}\n")