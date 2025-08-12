from tqdm import tqdm

from src.core.entities.event_bus.events import ProgressEvent
from src.core.enums import DownloadingType

_progress_bars: dict[str, tqdm] = {}

def progress_event_listener(event: ProgressEvent) -> None:
    if event.type == DownloadingType.INIT:
        bar = tqdm(total=event.total, desc=f"{event.id}", unit="B", unit_scale=True, leave=False, ncols=150)
        _progress_bars[event.id] = bar

    elif event.type == DownloadingType.IN_PROGRESS:
        bar = _progress_bars.get(event.id)
        if bar:
            delta = event.actual - bar.n
            bar.update(delta)

    elif event.type == DownloadingType.COMPLETED:
        bar = _progress_bars.get(event.id)
        if bar:
            bar.n = event.total
            bar.refresh()
            bar.close()
            print(f"{event.id}: download completed")

    elif event.type == DownloadingType.FAILED:
        bar = _progress_bars.get(event.id)
        if bar:
            bar.close()
        print(f"{event.id} download failed: {event.error_msg or 'unknown error'}")