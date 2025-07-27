from dependency_injector import containers, providers

from src.core.entities.observer import Subject


class Observers(containers.DeclarativeContainer):
    subject = providers.Factory(Subject)