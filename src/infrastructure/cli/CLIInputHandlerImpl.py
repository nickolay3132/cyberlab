from typing import List, Callable

from colorama.ansi import Fore

from src.core.interfaces.input.InputHandler import InputHandler


class CLIInputHandlerImpl(InputHandler):
    def select_option(self, data: List[str], callback: Callable[[int], None]) -> None:
        for index, value in enumerate(data):
            print(f"{index + 1}: {value}")

        selected_index = self._get_valid_index(min=1, max=len(data))
        callback(selected_index - 1)


    @staticmethod
    def _get_valid_index(min: int = 0, max: int = 1) -> int:
        while True:
            user_input = input(f"Select from {min} to {max}: ")

            if not user_input.isdigit():
                print(f"{Fore.RED}Invalid input. Try again.")
                continue

            index = int(user_input)

            if min <= index <= max:
                return index
            else:
                print(f"{Fore.RED}Index must be between {min} and {max}.")
                continue

        return -1