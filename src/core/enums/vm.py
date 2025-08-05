from enum import Enum


class NicType(Enum):
    NAT_NETWORK = 'natnetwork'
    INT_NETWORK = 'intnetwork'

class BootPolicyStartupType(Enum):
    GUI = 'gui'
    HEADLESS = 'headless'
    SEPARATE = 'separate'

class BootPolicyShutdownType(Enum):
    ACPI_POWER_BUTTON = 'acpipowerbutton'
    POWER_OFF = 'poweroff'
    SAVE_STATE = 'savestate'