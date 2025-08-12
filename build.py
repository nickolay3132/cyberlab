import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Callable
import pkg_resources


@dataclass
class BuildDto:
    filepath: Path
    binary_name: str
    add_data: List[Callable[[], str]]
    hide_console: bool = False
    icon_path: Path = None


def build(dto: BuildDto) -> None:
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", dto.binary_name,
        "--workpath", f"./tmp/{dto.binary_name}",
        "--specpath", f"./tmp/{dto.binary_name}",
    ]

    if dto.hide_console:
        cmd.append("--noconsole")

    if dto.icon_path and dto.icon_path.exists():
        cmd.append(f"--icon={dto.icon_path}")

    for f in dto.add_data:
        result = f()
        if result:  # skip empty strings
            cmd.append(result)

    cmd.append(str(dto.filepath))

    process = subprocess.Popen(cmd)
    process.wait()


def add_hidden_imports() -> str:
    packages = [dist.key for dist in pkg_resources.working_set]
    hidden_imports = [f"--hidden-import={p}" for p in packages]
    return ' '.join(hidden_imports)

if __name__ == "__main__":
    entry_point = Path(__file__).parent / "clmt.py"

    build_dto = BuildDto(
        filepath=entry_point,
        binary_name="clmt",
        add_data=[add_hidden_imports],
        hide_console=False,
        icon_path=Path(__file__).parent / "static" / "clmt-icon.ico"
    )

    build(build_dto)