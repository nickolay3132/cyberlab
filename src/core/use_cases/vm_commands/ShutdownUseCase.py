from dataclasses import dataclass

from src.core.entities.observer import Subject
from src.core.interfaces.services.vbox.VBoxManageService import VBoxManageService


@dataclass
class ShutdownUseCaseDTO:
    force: bool

@dataclass
class ShutdownUseCase:
    vboxmanage_service: VBoxManageService

    subject: Subject

    def execute(self, dto: ShutdownUseCaseDTO) -> None:
        self.vboxmanage_service.boot().shutdown(self.subject, force=dto.force)
        [self.subject.detach(observer) for observer in self.subject.observers]