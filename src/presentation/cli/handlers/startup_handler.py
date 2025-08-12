from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent
from src.core.use_cases import StartupUseCase, StartupUseCaseDto
from src.presentation.cli.event_listeners import text_event_listener


def handle_startup(args):
    use_case = get(StartupUseCase, f"{global_vars['root_dir']}/config.yaml")
    use_case.ev_bus.attach(TextEvent, text_event_listener)

    dto = StartupUseCaseDto()
    use_case.execute(dto)