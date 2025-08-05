import time
from dataclasses import dataclass

from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService
from src.core.use_cases.cyber_lab_info_use_case import CyberLabInfoUseCase


@dataclass
class ShutdownUseCaseDTO:
    force: bool

@dataclass
class ShutdownUseCase:
    vboxmanage_service: VBoxManageService

    info_use_case: CyberLabInfoUseCase

    def execute(self, dto: ShutdownUseCaseDTO) -> None:
        self.vboxmanage_service.boot().shutdown(force=dto.force)
        time.sleep(3)
        self.info_use_case.execute()