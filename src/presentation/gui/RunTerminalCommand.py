import os
import subprocess
from typing import List, Optional


class RunTerminalCommand:
    infinity = 99999

    def __init__(self, platform: str):
        self._platform = platform
        self.handlers = {
            'Windows': self.windows_exec,
            'Linux': self.linux_exec,
            'Darwin': self.mac_exec,
        }

    def exec(self, command: List[str], timeout: Optional[int] = 3) -> None:
        real_timeout = timeout if timeout is not None else self.infinity
        self.handlers.get(self._platform, self.unknown_exec)(command, real_timeout)

    @staticmethod
    def windows_exec(command: List[str], timeout: int = 10) -> None:
        bat_script = f"""
        @echo off
        {' '.join(command)}
        timeout /t {timeout} /nobreak >nul
        del "%~f0"
        exit
        """
        with open('temp_script.bat', "w") as f:
            f.write(bat_script)

        subprocess.Popen(['start', 'cmd', '/c', 'temp_script.bat'], shell=True)

    @staticmethod
    def linux_exec(command: List[str], timeout: int = 10) -> None:
        subprocess.Popen(['x-terminal-emulator', '-e',
                          f"bash -c '{' '.join(command)}; sleep {timeout}; exit'"])

    @staticmethod
    def mac_exec(command: List[str], timeout: int = 10) -> None:
        applescript = f"""
        tell application "Terminal"
            do script "{' '.join(command)}; sleep {timeout}; exit"
            delay {timeout + 1}
            quit
        end tell
        """
        subprocess.Popen(['osascript', '-e', applescript])

    def unknown_exec(self, command: List[str], timeout: int = 10) -> None:
        raise NotImplementedError(f"Unsupported OS: {self._platform}")