import src
from src.bootstrap import get, global_vars
from src.core.entities.event_bus.events import TextEvent, ProgressEvent
from src.core.use_cases import InstallUseCase, InstallUseCaseDto
from src.presentation.cli.event_listeners import text_event_listener, progress_event_listener


def handle_install(args):
    config_path = f"{global_vars['root_dir']}/config.yaml"
    snapshots_path = f"{global_vars['root_dir']}/snapshots.yaml"

    use_case = get(InstallUseCase, config_path, snapshots_path)
    use_case.ev_bus.attach(TextEvent, text_event_listener)
    use_case.ev_bus.attach(ProgressEvent, progress_event_listener)

    dto = InstallUseCaseDto(
        repository=src.__repository__,
        skip_download=args.skip_download,
        no_verify=args.no_verify
    )

    use_case.execute(dto)