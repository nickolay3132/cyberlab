from typing import Type, Callable

_BIND_REGISTRY: dict[Type, Callable] = {}

def register(type_: Type, func: Callable):
    _BIND_REGISTRY[type_] = func

def get(type_: Type) -> Callable:
    func = _BIND_REGISTRY.get(type_)
    if func is None:
        raise ValueError(f"Bind for type {type_.__name__} not found")
    return func