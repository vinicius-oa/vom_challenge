""" Dependency Injection Setup. """
from queue import Queue

from dependency_injector import containers, providers

from domain.common.repository.entities import PolicyEntity
from domain.config_backend.repositories.config_backend import (
    ConfigBackendRepository
)
from domain.config_backend.services.config_backend import ConfigBackendService
from domain.config_backend.services.config_backend.validators.policy_flow.validators import (  # noqa
    PolicyFlowValidator
)
from domain.execution_engine.services.execution_engine import (
    ExecutionEngineService
)
from infra.database.factory.factory import DatabaseFactory


class DI(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
           "domain.config_backend.controllers.config_backend",
           "domain.execution_engine.controllers.execution_engine"
        ]
    )

    stream_execution_engine_queue = providers.Singleton(Queue)

    # Factories
    # # Register available databases by importing
    from infra.database.sqlite import SqliteDatabase # noqa

    _database_factory = providers.Singleton(DatabaseFactory)
    _database_to_assemble = _database_factory().get_database()
    database = providers.Singleton(
        _database_to_assemble["db"],
        **_database_to_assemble["kwargs"]
    )

    # Repositories
    config_backend_repository = providers.Singleton(
        ConfigBackendRepository,
        database=database,
        entity=PolicyEntity
    )

    # Services
    config_backend_service = providers.Singleton(
        ConfigBackendService,
        repository=config_backend_repository,
        policy_flow_validator=PolicyFlowValidator,
        stream_execution_engine_queue=stream_execution_engine_queue
    )
    execution_engine_service = providers.Factory(
        ExecutionEngineService,
        config_backend_repository=config_backend_repository,
        stream_execution_engine_queue=stream_execution_engine_queue
    )
