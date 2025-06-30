import pyfiglet
from colorama.ansi import Fore, Style

from src import __version__


class BaseTexts:
    @staticmethod
    def hello():
        ascii_title = pyfiglet.figlet_format("CyberLab CLI", font="slant")
        description = "Cyber Lab management tool".rjust(68)
        version = __version__.rjust(68)

        header = [
            f"{Fore.BLUE}{ascii_title}",
            f"{Fore.WHITE}{"━" * 68}",
            f"{description}",
            f"{Fore.YELLOW}{version}",
        ]

        print("\n".join(header))