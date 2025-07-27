from dependency_injector import containers, providers

from src.infrastructure.containers.Commands import Commands
from src.infrastructure.containers.Repos import Repos
from src.infrastructure.containers.Services import Services
from src.infrastructure.containers.UseCases import UseCases
from src.infrastructure.containers.event_bus import CliEventListenerContainer, EventBusContainer


class CliMainContainer(containers.DeclarativeContainer):
    event_listeners = providers.Container(CliEventListenerContainer)
    event_bus_container = providers.Container(EventBusContainer, event_listeners=event_listeners)

    repositories = providers.Container(Repos)
    services = providers.Container(Services, repos=repositories, event_buses=event_bus_container)
    use_cases = providers.Container(UseCases, services=services, event_buses=event_bus_container)
    commands = providers.Container(Commands, use_cases=use_cases)

