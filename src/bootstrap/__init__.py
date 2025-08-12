import importlib
import pkgutil

from .registry import get

global_vars = {}

def bootstrap():
    import src.bootstrap.factories.event_bus
    import src.bootstrap.factories.gateways
    import src.bootstrap.factories.repositories
    import src.bootstrap.factories.services
    import src.bootstrap.factories.use_cases