from colorama.ansi import Fore

from src.texts.BaseTexts import BaseTexts


class CreateTexts (BaseTexts):
    @staticmethod
    def vm_not_exist(vm_name):
        print(f"{Fore.RED}Virtual machine '{vm_name}' does not exist.")
