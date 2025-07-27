from colorama.ansi import Fore, Style
from tqdm import tqdm

from src.core.entities.event_bus import EventListener, Event
from src.core.entities.event_bus.events import ProgressEvent, ProgressEventStates


class ProgressEventListener(EventListener[ProgressEvent]):
    def __init__(self) -> None:
        self.pbar = None

    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        pass

    def on_event(self, event: ProgressEvent) -> None:
        if event.type == ProgressEventStates.INIT:
            print(f"{event.id}: Downloading...")
            self.pbar = tqdm(total=event.total, unit="B", unit_scale=True, ncols=100)

        if event.type == ProgressEventStates.IN_PROGRESS:
            self.pbar.update(event.actual - self.pbar.n)

        if event.type == ProgressEventStates.COMPLETED:
            self.pbar.close()
            print()

        if event.type == ProgressEventStates.ERROR:
            self.pbar.close()
            print(f"{event.id}: {Fore.RED}Downloading error.{Style.RESET_ALL} {event.error_message}")