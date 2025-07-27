from colorama.ansi import Fore

from src.core.entities.observer import ObserverEvent
from src.presentation.cli.observers.cli_observer_invoker import CLIObserverInvoker


class TextsCLIObserver(CLIObserverInvoker):
    def __init__(self):
        super().__init__()

        self.add_event_handlers({
            'title': self.title_event,
            'success': self.success_event,
            'text': self.text_event,
            'space': self.space_event,
            'warning': self.warning_event,
            'error': self.error_event
        })

    @staticmethod
    def title_event(event: ObserverEvent):
        print(f"{Fore.CYAN}{event.data}")

    @staticmethod
    def success_event(event: ObserverEvent):
        print(f"{Fore.GREEN}{event.data}")

    @staticmethod
    def text_event(event: ObserverEvent):
        print(event.data)

    @staticmethod
    def space_event(event: ObserverEvent):
        print()

    @staticmethod
    def warning_event(event: ObserverEvent):
        print(f"{Fore.YELLOW}{event.data}")

    @staticmethod
    def error_event(event: ObserverEvent):
        print(f"{Fore.RED}{event.data}")