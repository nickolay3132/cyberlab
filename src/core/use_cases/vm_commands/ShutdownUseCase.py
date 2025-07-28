from dataclasses import dataclass

from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService


@dataclass
class ShutdownUseCaseDTO:
    force: bool

@dataclass
class ShutdownUseCase:
    vboxmanage_service: VBoxManageService

    def execute(self, dto: ShutdownUseCaseDTO) -> None:
        self.vboxmanage_service.boot().shutdown(force=dto.force)
        pass