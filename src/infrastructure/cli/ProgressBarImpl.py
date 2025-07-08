from src.core.interfaces.output.ProgressBar import ProgressBar
from tqdm import tqdm


class ProgressBarImpl(ProgressBar):
    def __init__(self):
        self._pbar = None

    def update(self, current: int, total: int) -> None:
        if self._pbar is None:
            self._pbar = tqdm(total=total, unit="B", unit_scale=True)
        self._pbar.update(current - self._pbar.n)

    def close(self) -> None:
        if self._pbar:
            self._pbar.close()