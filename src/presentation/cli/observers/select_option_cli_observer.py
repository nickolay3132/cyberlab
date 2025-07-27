from asyncio import Future
from typing import List

from colorama.ansi import Fore

from src.core.entities.observer import ObserverEvent
from src.presentation.cli.observers.cli_observer_invoker import CLIObserverInvoker


class SelectOptionCLIObserver(CLIObserverInvoker):
    def __init__(self):
        super().__init__()

        self.add_event_handlers({
            'select_option': self.select_option_event
        })

    def select_option_event(self, event: ObserverEvent):
        options: List[str] = event.data['options']
        future: Future = event.data['future']

        for index, value in enumerate(options):
            print(f'{index + 1}: {value}')

        selected_option = self.get_valid_index(1, len(options))
        future.set_result(selected_option)

    @staticmethod
    def get_valid_index(min_val: int = 0, max_val: int = 1):
        while True:
            usr_input = input(f'Select from {min_val} to {max_val}: ')

            if not usr_input.isdigit():
                print(f'{Fore.RED}Invalid input. Try again.')
                continue

            index = int(usr_input)
            if min_val <= index <= max_val:
                return index
            else:
                print(f"Index must be between {min_val} and {max_val}.")
                continue
        return -1