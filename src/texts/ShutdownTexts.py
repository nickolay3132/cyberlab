from colorama.ansi import Fore

from src.texts.BaseTexts import BaseTexts


class ShutdownTexts (BaseTexts):
    @staticmethod
    def force_shutdown(vm_name):
        print(f"{Fore.YELLOW}{vm_name} will shutdown immediately")

    @staticmethod
    def shutdown(vm_name: str):
        print(f"{Fore.CYAN}Stopping {vm_name}...")

    @staticmethod
    def failed_to_stop(vm_name):
        print(f"{Fore.RED}Failed to stop virtual machine {vm_name}")
