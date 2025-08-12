import argparse
import sys
from pathlib import Path

from src.bootstrap import bootstrap, global_vars


def init_cli():
    from src.presentation.cli import (
        register_install_command,
        register_startup_command,
        register_shutdown_command,
        register_snapshot_commands,
    )

    parser = argparse.ArgumentParser(prog="clmt", description="CyberLab Management Tool CLI")
    subparsers = parser.add_subparsers(dest="command")

    register_install_command(subparsers)
    register_startup_command(subparsers)
    register_shutdown_command(subparsers)
    register_snapshot_commands(subparsers)

    args = parser.parse_args(sys.argv[2:])

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)

def init_gui():
    from PyQt6.QtGui import QFontDatabase, QFont
    from PyQt6.QtWidgets import QApplication
    from src.presentation.gui.ui import MainWindow

    app = QApplication([])

    font_id = QFontDatabase.addApplicationFont(f"{global_vars['root_dir']}/static/fonts/FragmentMono-Regular.ttf")
    font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
    global_vars['font'] = QFont(font_name, 11)
    global_vars['btn_font'] = QFont(font_name, 9)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

def main():
    if 'cli' in sys.argv:
        init_cli()
    else:
       init_gui()

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        global_vars['root_dir'] = Path(sys.executable).parent
    else:
        global_vars['root_dir'] = Path(__file__).resolve().parent

    bootstrap()
    main()