from dataclasses import dataclass

from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService


@dataclass
class StartupCommandDTO:
    pass

@dataclass
class StartupCommand:
    vboxmanage_service: VBoxManageService

    def execute(self, dto: StartupCommandDTO):
        self.vboxmanage_service.boot().startup()