from enum import Enum
from typing import Dict

from src.core.entities.event_bus.events import ProgressEvent, ProgressEventStates
from src.presentation.gui.event_listeners import BaseEventListener
from src.presentation.gui.widgets.progress_bar_widget import ProgressBarWidget


class ProgressEventListener(BaseEventListener[ProgressEvent]):
    def __init__(self, layout_map):
        super().__init__(layout_map)

        self.progress_bars: Dict[str | Enum, ProgressBarWidget] = {}

        self.add_event_handlers({
            ProgressEventStates.INIT: self.init_progress,
            ProgressEventStates.IN_PROGRESS: self.update_progress,
            ProgressEventStates.COMPLETED: self.complete_progress,
            ProgressEventStates.ERROR: self.progress_error,
        })

        self.add_skip_clear_for_event(ProgressEventStates.INIT)
        self.add_skip_clear_for_event(ProgressEventStates.IN_PROGRESS)
        self.add_skip_clear_for_event(ProgressEventStates.COMPLETED)
        self.add_skip_clear_for_event(ProgressEventStates.ERROR)

    def init_progress(self, event: ProgressEvent):
        if not event.id in self.progress_bars:
            self.progress_bars[event.id] = ProgressBarWidget()
            layout = self._layout_map[event.id]
            self._clear_layout(layout)

        return self.progress_bars[event.id]

    def update_progress(self, event: ProgressEvent):
        if not event.id in self.progress_bars:
            self.progress_bars[event.id] = ProgressBarWidget()
        pb = self.progress_bars[event.id]
        pb.update_progress(event.total, event.actual)
        return pb

    def complete_progress(self, event: ProgressEvent):
        pb = self.progress_bars[event.id]
        pb.completed()
        return pb

    def progress_error(self, event: ProgressEvent):
        pb = self.progress_bars[event.id]
        pb.error(event.error_message)
        return pb

