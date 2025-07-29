import time
from dataclasses import dataclass

from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService
from src.core.use_cases.cyber_lab_info_use_case import CyberLabInfoUseCase


@dataclass
class StartupUseCaseDTO:
    pass

@dataclass
class StartupUseCase:
    vboxmanage_service: VBoxManageService

    info_use_case: CyberLabInfoUseCase

    def execute(self, dto: StartupUseCaseDTO):
        self.vboxmanage_service.boot().startup()

        time.sleep(3)
        self.info_use_case.execute()