from enum import Enum


class TextEventType(Enum):
    TEXT = 'text'
    TITLE = 'title'
    SUCCESS = 'success'
    SPACE = 'space'
    WARNING = 'warning'
    ERROR = 'error'