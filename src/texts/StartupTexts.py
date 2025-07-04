from colorama.ansi import Fore

from src.texts.BaseTexts import BaseTexts


class StartupTexts (BaseTexts):
    @staticmethod
    def failed_to_start(vm_name):
        print(f"{Fore.RED}Failed to start virtual machine {vm_name}\n")