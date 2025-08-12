from src.core.entities.event_bus.events import TextEvent
from src.core.enums.events import TextEventType


# ANSI color codes
COLOR_CODES = {
    TextEventType.TITLE: '\033[36m',    # Cyan
    TextEventType.SUCCESS: '\033[32m',  # Green
    TextEventType.WARNING: '\033[33m',  # Yellow
    TextEventType.ERROR: '\033[31m',    # Red
    TextEventType.TEXT: '',             # No color
}

RESET = '\033[0m'

def text_event_listener(event: TextEvent) -> None:
    if event.type == TextEventType.SPACE:
        print()
        return

    prefix = ''
    if event.id not in ['main', 'dialog']:
        prefix = f"{event.id}: "

    color = COLOR_CODES.get(event.type, '')
    output = f"{prefix}{event.text}"

    if color:
        output = f"{color}{output}{RESET}"

    print(output)