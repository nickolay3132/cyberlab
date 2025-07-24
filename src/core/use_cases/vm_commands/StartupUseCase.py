from dataclasses import dataclass

from src.core.entities.observer import Subject
from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService


@dataclass
class StartupUseCaseDTO:
    pass

@dataclass
class StartupUseCase:
    vboxmanage_service: VBoxManageService

    subject: Subject = Subject()

    def execute(self, dto: StartupUseCaseDTO):
        self.vboxmanage_service.boot().startup(self.subject)