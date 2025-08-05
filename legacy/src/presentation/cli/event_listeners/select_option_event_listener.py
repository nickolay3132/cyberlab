from colorama.ansi import Fore

from src.core.entities.event_bus import EventListener
from src.core.entities.event_bus.events import SelectOptionEvent


class SelectOptionEventListener(EventListener[SelectOptionEvent]):
    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        pass

    def on_event(self, event: SelectOptionEvent) -> None:
        for index, option in enumerate(event.options):
            print(f"{index + 1}: {option}")

        selected_option = self.get_valid_index(1, len(event.options))
        event.future.set_result(selected_option)

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
                print(f"{Fore.RED}Index must be between {min_val} and {max_val}.")
                continue
        return -1