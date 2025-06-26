import os
from pathlib import Path

import requests
from tqdm import tqdm


class Utils:
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

        print(f"\nDownloading to {os.path.basename(path)}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192

            with open(path, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                    for chunk in response.iter_content(chunk_size=block_size):
                        f.write(chunk)
                        pbar.update(len(chunk))
        except Exception as e:
            print(f"\nError fetching url: {url}\n{str(e)}")

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