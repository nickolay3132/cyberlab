import pyfiglet
from colorama.ansi import Fore, Style

from src import __version__


class BaseTexts:
    @staticmethod
    def hello():
        ascii_title = pyfiglet.figlet_format("CyberLab CLI", font="slant")
        description = "cli sfsdfsdfsdf sdfsdfsdf".rjust(68)
        version = __version__.rjust(68)

        header = [
            f"{Fore.BLUE}{ascii_title}{Style.RESET_ALL}",
            f"{Fore.WHITE}{"━" * 68}",
            f"{description}",
            f"{Fore.YELLOW}{version}{Style.RESET_ALL}",
        ]

        print("\n".join(header))