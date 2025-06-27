import sys

import yaml


def get_vms(path: str) -> list[list[str]]:
    result = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                stripped_line = line.strip()

                if not stripped_line or stripped_line.startswith(';'):
                    continue

                parts = [part.strip() for part in stripped_line.split(':', 1)]

                if len(parts) != 2 or not all(parts):
                    print(f"Warning: invalid format at line {line_number} - '{stripped_line}'. Skipping.")
                    continue

                result.append(parts)

    except FileNotFoundError:
        print(f"Error: file '{path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    return result

def get_virtual_machines(path: str) -> list[dict[str, any]]:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get('virtual_machines', [])
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error while reading YAML: {e}")