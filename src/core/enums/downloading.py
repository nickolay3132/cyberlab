from enum import Enum


class DownloadingType(Enum):
    INIT = 'init'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'