from dataclasses import dataclass

from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService


@dataclass
class ShutdownCommandDTO:
    force: bool

@dataclass
class ShutdownCommand:
    vboxmanage_service: VBoxManageService

    def execute(self, dto: ShutdownCommandDTO) -> None:
        self.vboxmanage_service.boot().shutdown(force=dto.force)