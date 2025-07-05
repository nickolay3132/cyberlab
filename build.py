import os
import subprocess
import sys
from pathlib import Path
import pyfiglet


def build_cyberlab():
    script_path = Path(__file__).parent / "cyberlab.py"

    fonts_dir = Path(pyfiglet.__file__).parent / "fonts"
    fonts_src = str(fonts_dir)
    fonts_dest = "pyfiglet/fonts"

    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "cyberlab",  # Имя выходного файла (без .exe)
        f"--add-data={fonts_src}{os.pathsep}{fonts_dest}",
        "--hidden-import=pyfiglet.fonts",
        "--workpath", "./tmp",
        "--specpath", "./tmp",
        str(script_path)
    ]

    print("Start Packaging...")
    print("Command:", " ".join(cmd))
    result = subprocess.run(cmd, check=False)

    if result.returncode == 0:
        print(f"Packaging finished!")
    else:
        print("Error during packaging!")
        sys.exit(1)

if __name__ == "__main__":
    build_cyberlab()