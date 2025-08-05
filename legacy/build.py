import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Callable

import pkg_resources

import pyfiglet


@dataclass
class BuildDto:
    filepath: Path
    binary_name: str

def build(dto: BuildDto, add_data: List[Callable[[], str]]) -> None:
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", dto.binary_name,
        "--collect-submodules=dependency_injector",
        "--hidden-import=pyfiglet.fonts",
        "--workpath", f"./tmp/{dto.binary_name}",
        "--specpath", f"./tmp/{dto.binary_name}",
    ]

    [cmd.append(f()) for f in add_data]
    cmd.append(str(dto.filepath))

    subprocess.run(cmd, check=True)

def add_dependency_injector() -> str:
    return '--collect-submodules=dependency_injector'

def add_hidden_imports() -> str:
    packages = [dist.key for dist in pkg_resources.working_set]
    hidden_imports = [f"--hidden-import={p}" for p in packages]
    hidden_imports.append("--hidden-import=pyfiglet.fonts")

    return ' '.join(hidden_imports)

def add_fonts() -> str:
    fonts_dir = Path(pyfiglet.__file__).parent / "fonts"
    fonts_src = str(fonts_dir)
    fonts_dest = "pyfiglet/fonts"

    return f"--add-data={fonts_src}{os.pathsep}{fonts_dest}"

def add_icon() -> str:
    icon_path = Path(__file__).parent / "cyberlab-icon.ico"
    return f"--icon={str(icon_path)}"

def hide_console() -> str:
    return '--noconsole'


if __name__ == "__main__":
    cli_build_dto = BuildDto(
        filepath=Path(__file__).parent / "cyberlab_cli.py",
        binary_name="CyberLabCli",
    )

    build(cli_build_dto, [add_dependency_injector, add_hidden_imports, add_fonts])

    gui_build_dto = BuildDto(
        filepath=Path(__file__).parent / "cyberlab.py",
        binary_name="CyberLab",
    )

    build(gui_build_dto, [add_dependency_injector, add_hidden_imports, add_fonts, add_icon, hide_console])