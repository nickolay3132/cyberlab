from typing import Dict

from PyQt6.QtWidgets import QApplication

from src.core.entities.event_bus import EventListener
from src.core.entities.event_bus.events import SelectOptionEvent
from src.presentation.gui.event_listeners import EventListenerGuiSignalBridge
from src.presentation.gui.widgets.select_dialog_widget import SelectDialogWidget


class SelectOptionEventListener(EventListener[SelectOptionEvent]):
    def __init__(self):
        self.signal = EventListenerGuiSignalBridge(self.handle_event)
        self.dialogs: Dict[str, SelectDialogWidget] = {}

    def on_attach(self) -> None:
        pass

    def on_detach(self) -> None:
        self.dialogs.clear()

    def on_event(self, event: SelectOptionEvent) -> None:
        self.signal.emit(event)

    def handle_event(self, event: SelectOptionEvent) -> None:
        for dialog in self.dialogs.values():
            dialog.close()

        if event.id not in self.dialogs:
            dialog = SelectDialogWidget(
                options=event.options,
                future=event.future,
                parent=QApplication.activeWindow()
            )
            dialog.exec()
            self.dialogs[event.id] = dialog
        return