from queue import Queue
from typing import Type, TYPE_CHECKING

from domain.config_backend.services.config_backend.validators.policy_flow.validators import (  # noqa
    PolicyFlowValidator
)

if TYPE_CHECKING:
    from domain.config_backend.controllers.schemas.request.config_backend import (  # noqa
        ConfigBackendCreatePolicyRequest,
        ConfigBackendUpdatePolicyRequest
    )
    from domain.config_backend.repositories.config_backend import (
        ConfigBackendRepository
    )


class ConfigBackendService:

    def __init__(
        self,
        *,
        repository: "ConfigBackendRepository",
        policy_flow_validator: Type[PolicyFlowValidator],
        stream_execution_engine_queue: Queue
    ):
        self._repository = repository
        self._policy_flow_validator = policy_flow_validator
        self._stream_execution_engine_queue = stream_execution_engine_queue

    def create_policy(self, value: "ConfigBackendCreatePolicyRequest"):
        self._policy_flow_validator(value.policy_flow)
        return self._repository.create_policy(value)

    def read_policy(self, id_: int):
        return self._repository.read_policy(id_)

    def read_all_policies(self):
        return self._repository.read_all_policies()

    def update_policy(
        self,
        id_: int,
        value: "ConfigBackendUpdatePolicyRequest"
    ):
        if value.policy_flow is not None:
            self._policy_flow_validator(value.policy_flow)
        result = self._repository.update_policy(id_, value)
        self._stream_execution_engine_queue.put_nowait(result.id)
        return result
