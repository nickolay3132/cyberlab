import yaml


def get_full_config(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error while reading YAML: {e}")

def get_virtual_machines(path: str) -> list[dict[str, any]]:
   return get_full_config(path)['virtual_machines']