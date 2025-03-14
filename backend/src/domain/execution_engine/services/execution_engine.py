import asyncio
import json
import queue
from contextlib import suppress
from copy import deepcopy
from queue import Queue
from typing import Optional, TYPE_CHECKING

from sse_starlette import ServerSentEvent
from starlette import status
from starlette.datastructures import QueryParams
from starlette.requests import Request

from domain.common.enums.blocks_properties import PolicyBlockTypesEnum
from domain.common.service.exceptions import ServiceException
from domain.config_backend.repositories.config_backend import (
    ConfigBackendRepository
)
from domain.execution_engine.enums.error_messages import (
    ExceptionErrorMsgs as ErrMsg
)

if TYPE_CHECKING:
    from domain.common.repository.entities import (
        PolicyEntity,
        PolicyEntityPolicyFlow
    )


class ExecutionEngineService:

    def __init__(
        self,
        *,
        config_backend_repository: "ConfigBackendRepository",
        stream_execution_engine_queue: Queue
    ):
        self._config_backend_repository = config_backend_repository
        self._blocks_variable_name_property = set()
        self._stream_execution_engine_queue = stream_execution_engine_queue

    def _validate_policy_input_values(
        self,
        policy: "PolicyEntity",
        input_values: QueryParams
    ):
        """
            `values` must match the policy's blocks' property `variable_name`
        """
        policy_flow = policy.parse_policy_flow()

        # domain.config_backend.services.config_backend.validators.policy_flow.validators.PolicyFlowValidator.__docs__
        first_condition_block = policy_flow.block_targets[0]
        self._blocks_variable_name_property.add(
            first_condition_block.variable_name
        )

        self._find_all_blocks_variable_name_property(first_condition_block)

        # cleans up as this object may still exist when a policy is changed.
        blocks_variable_name_property = deepcopy(
            self._blocks_variable_name_property
        )
        self._blocks_variable_name_property.clear()

        input_variables_names = set(input_values.keys())
        if input_variables_names != blocks_variable_name_property:
            raise ServiceException(
                content=ErrMsg.EXECUTION_ENGINE_INVALID_QUERY_PARAMS,
                status_code=status.HTTP_400_BAD_REQUEST,
                additional_content="input_values_does_not_match_policy"
            )

    def _find_all_blocks_variable_name_property(
        self,
        block: "PolicyEntityPolicyFlow"
    ):
        for b in block.block_targets:
            # domain.config_backend.services.config_backend.validators.policy_flow.enums.blocks_properties
            # Only blocks of type `condition` have such property.
            if b.block_type == PolicyBlockTypesEnum.condition:
                self._blocks_variable_name_property.add(b.variable_name)
                self._find_all_blocks_variable_name_property(b)

    def validate_input_values(
        self,
        *,
        policy_id: int,
        input_values: QueryParams
    ):
        policy = self._config_backend_repository.read_policy(policy_id)
        self._validate_policy_input_values(policy, input_values)
        return policy

    async def execute_policy(
        self,
        request: Request,
        policy: "PolicyEntity",
        input_values: QueryParams   # noqa
    ):
        # The queue may not be empty, so clean it up first.
        with suppress(queue.Empty):
            while True:
                if self._stream_execution_engine_queue.empty():
                    break
                self._stream_execution_engine_queue.get_nowait()

        def evaluate_policy(
            p: "PolicyEntity",
            updated: bool = False
        ) -> ServerSentEvent:
            if updated:
                # Policy has been updated, so there will be a new evaluation of it.  # noqa
                delattr(self, "_policy_decision")

                p = self._config_backend_repository.read_policy(p.id)
                try:
                    self._validate_policy_input_values(p, input_values)
                except ServiceException:
                    return ServerSentEvent(
                        event="error",
                        data=json.dumps({
                            "error": "The passed query parameters' names"
                                     " do not match the policy anymore."
                                     " Please, try again."
                        })
                    )
            self._evaluate_policy(p, input_values)
            return ServerSentEvent(
                data=json.dumps({'decision': self._policy_decision})
            )

        yield evaluate_policy(policy)

        flag = True
        while flag:
            if await request.is_disconnected():
                break
            if not self._stream_execution_engine_queue.empty():
                policy_id = self._stream_execution_engine_queue.get_nowait()
                if policy_id == policy.id:
                    result = evaluate_policy(policy, updated=True)
                    if result.event == "error":
                        flag = False
                    yield result
            await asyncio.sleep(0.1)

    def _evaluate_policy(
        self,
        policy: "PolicyEntity",
        input_values: QueryParams
    ):
        policy_flow = policy.parse_policy_flow()
        # domain.config_backend.services.config_backend.validators.policy_flow.validators.PolicyFlowValidator.__docs__
        first_condition_block = policy_flow.block_targets[0]
        self._evaluate_policy_decision(first_condition_block, input_values)

    def _evaluate_policy_decision(
        self,
        block: "PolicyEntityPolicyFlow",
        input_values: QueryParams,
        flow: Optional[bool] = None # noqa
    ):
        """
            The policy's flow will be evaluated until
            a block of type `end` is reached.
        """
        input_value = float(input_values.get(block.variable_name))
        python_operator = block.variable_operator.get_python_operator()
        flow = python_operator(input_value, block.variable_value)
        block_target_to_evaluate = next(
            x for x in block.block_targets if x.flow == flow
        )
        if block_target_to_evaluate.block_type == PolicyBlockTypesEnum.end:
            self._policy_decision = block_target_to_evaluate.output
            return
        self._evaluate_policy_decision(block_target_to_evaluate, input_values)
