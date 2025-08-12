from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent
from src.core.use_cases import ShutdownUseCase, ShutdownUseCaseDto
from src.presentation.cli.event_listeners import text_event_listener


def handle_shutdown(args):
    use_case = get(ShutdownUseCase, f"{global_vars['root_dir']}/config.yaml")
    use_case.ev_bus.attach(TextEvent, text_event_listener)

    dto = ShutdownUseCaseDto(args.force)
    use_case.execute(dto)