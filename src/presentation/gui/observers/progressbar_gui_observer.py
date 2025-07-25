from src.core.entities.observer import ObserverEvent
from src.presentation.gui.observers.gui_observer_invoker import GUIObserverInvoker
from src.presentation.gui.widgets.progress_bar_widget import ProgressBarWidget


class ProgressBarGuiObserver(GUIObserverInvoker):
    def __init__(self, layouts_map):
        super().__init__(layouts_map)
        
        self.progress_bars = {}
        self.add_event_handlers({
            "progress": self.progress_bar_event
        })
        self.add_skip_clear_for_event("progress")
        
    def progress_bar_event(self, event: ObserverEvent):
        if not event.id in self.progress_bars:
            pb_widget = ProgressBarWidget(download_id=event.id)
            pb_widget.setMinimumHeight(30)
            pb_widget.setMaximumHeight(30)

            self.progress_bars[event.id] = pb_widget

        self.progress_bars[event.id].update_progress(event.data)
        return self.progress_bars[event.id]