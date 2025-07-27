from typing import Callable, Dict

from colorama.ansi import Fore

from src.core.entities.observer import Observer, ObserverEvent, Subject


class CLIObserverInvoker(Observer):
    def __init__(self) -> None:
        self._event_handlers: Dict[str, Callable[[ObserverEvent], None]] = {}

    def update(self, event: ObserverEvent) -> None:
        handler = self._event_handlers.get(event.type, self.unknown_event)
        handler(event)

    def on_detach(self) -> None:
        print(f"{Fore.GREEN}All operations completed")

    def add_event_handlers(self, handler: Dict[str, Callable[[ObserverEvent], None]]) -> None:
        self._event_handlers.update(handler)

    def unknown_event(self, event: ObserverEvent) -> None:
        pass
