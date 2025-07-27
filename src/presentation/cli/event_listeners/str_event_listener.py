from colorama.ansi import Fore

from src.core.entities.event_bus import EventListener
from src.core.entities.event_bus.events import StrEvent, StrEventTypes


class StrEventListener(EventListener[StrEvent]):
    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        pass

    def on_event(self, event: StrEvent) -> None:
        if event.type == StrEventTypes.TITLE:
            print(f"{self.get_prefix(event.id)}{Fore.CYAN}{event.data}")

        if event.type == StrEventTypes.TEXT:
            print(f"{self.get_prefix(event.id)}{event.data}")

        if event.type == StrEventTypes.SUCCESS:
            print(f"{self.get_prefix(event.id)}{Fore.GREEN}{event.data}")

        if event.type == StrEventTypes.WARNING:
            print(f"{self.get_prefix(event.id)}{Fore.YELLOW}{event.data}")

        if event.type == StrEventTypes.ERROR:
            print(f"{self.get_prefix(event.id)}{Fore.RED}{event.data}")

        if event.type == StrEventTypes.SPACE:
            print()

    @staticmethod
    def get_prefix(ev_id: str) -> str:
        skip_ev_ids = ('main', )
        return f"{ev_id}: " if ev_id not in skip_ev_ids else ""