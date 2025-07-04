from colorama.ansi import Fore

from src.texts.BaseTexts import BaseTexts


class InstallTexts (BaseTexts):
    @staticmethod
    def downloading_started():
        print(Fore.CYAN + "\n=== DOWNLOADING VMS ===")

    @staticmethod
    def file_already_downloaded(name):
        print(Fore.GREEN + f"{name} already downloaded")

    @staticmethod
    def importing_started():
        print(Fore.CYAN + "\n=== IMPORTING VMS ===")

    @staticmethod
    def vm_already_exists(vm_name):
        print(Fore.YELLOW + f"{vm_name} already imported! Skipping...")

    @staticmethod
    def error_importing_vm(vm_name, error_msg = ""):
        print(Fore.RED + f"\nError importing {vm_name}{'!' if error_msg == '' else f':{error_msg}'}")

    @staticmethod
    def all_operations_completed():
        print(Fore.GREEN + "\nAll operations completed!")

