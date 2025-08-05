from .registry import register

def bind(func):
    return_type = getattr(func, '__annotations__', {}).get('return')
    if return_type is None:
        raise ValueError("Fabric function must have return type hint")
    register(return_type, func)
    return func

