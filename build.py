import os
import subprocess
from pathlib import Path

import pkg_resources

import pyfiglet

class Build:
    @staticmethod
    def run() -> None:
        cli_path = Path(__file__).parent / "cyberlab_cli.py"
        gui_path = Path(__file__).parent / "cyberlab.py"

        Build.build_script(cli_path, 'cyberlab_cli')
        Build.build_script(gui_path, 'cyberlab')

    @staticmethod
    def build_script(filepath: Path, binary_name: str) -> None:
        fonts_dir = Path(pyfiglet.__file__).parent / "fonts"
        fonts_src = str(fonts_dir)
        fonts_dest = "pyfiglet/fonts"

        packages = [dist.key for dist in pkg_resources.working_set]
        hidden_imports = [f"--hidden-import={p}" for p in packages]

        cmd = [
            "pyinstaller",
            "--onefile",
            "--name", binary_name,
            "--collect-submodules=dependency_injector",
            ''.join(hidden_imports),
            f"--add-data={fonts_src}{os.pathsep}{fonts_dest}",
            "--hidden-import=pyfiglet.fonts",
            "--workpath", f"./tmp/{binary_name}",
            "--specpath", f"./tmp/{binary_name}",
            str(filepath)
        ]

        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    Build.run()