from abc import ABC

from src.core.entities.event_bus import EventBuilder


class Event[B: EventBuilder](ABC): pass