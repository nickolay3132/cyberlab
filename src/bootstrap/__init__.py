import importlib
import pkgutil

from .registry import get

global_vars = {}

def bootstrap():
    import src.bootstrap.factories

    for loader, name, is_pkg in pkgutil.iter_modules(src.bootstrap.factories.__path__):
        full_name = f"{src.bootstrap.factories.__name__}.{name}"
        importlib.import_module(full_name)