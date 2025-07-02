import os
from pathlib import Path

import requests
from tqdm import tqdm

class Utils:
    @staticmethod
    def print_cli_hello():
        print("=== CyberLab CLI ===\n")
        print("This utility helps you to manage your CyberLab virtual machines.\n")
        print(f"{"=" * 64}\n")

    @staticmethod
    def to_absolute_path(path: str) -> str:
        expanded_path = os.path.expanduser(path)

        if os.path.isabs(expanded_path):
            return os.path.normpath(expanded_path)
        else:
            return os.path.normpath(os.path.join(os.getcwd(), expanded_path))

    @staticmethod
    def mkdirs(*path):
        for p in path:
            if not os.path.exists(p):
                os.makedirs(p)

    @staticmethod
    def fetch_file(url: str, path: str, check_if_exists=False):

        if check_if_exists:
            if os.path.exists(path):
                print(f"File {os.path.basename(path)} already exists! Skipping...")
                return

        print(f"\nDownloading {os.path.basename(path)}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192

            # instead of writing directly into file, we first write it into
            # a temporary buffer and only if the download is completed
            # successfully, we rename it afterwards.
            # It allows us to determine which files are corrupted if download
            # gets interrupted.
            temp_path = f'{path}.tmp'
            with open(temp_path, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    for chunk in response.iter_content(chunk_size=block_size):
                        f.write(chunk)
                        pbar.update(len(chunk))

            os.rename(temp_path, path)

        except KeyboardInterrupt as interrupt:
            # (Andrew) TODO: add keyboard interruption handling
            print("Download has been interrupted")
            os.remove(temp_path)

        except Exception as e:
            print(f"\nError fetching url: {url}\n{str(e)}")
            os.remove(temp_path)

    @staticmethod
    def find_files(directory: str, *extensions: str) -> list[tuple[str, str]]:
        try:
            dir_path = Path(directory).absolute()
            normalized_exts = {f".{ext.lower().lstrip('.')}" for ext in extensions}

            return [
                (file.stem, str(file))
                for file in dir_path.rglob('*')
                if file.is_file() and file.suffix.lower() in normalized_exts
            ]

        except Exception as e:
            print(f"Error scanning directory: {e}")
            return []
