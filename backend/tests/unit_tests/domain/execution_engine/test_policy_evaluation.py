import json
from contextlib import nullcontext as does_not_raise_exception
from copy import deepcopy
from types import MappingProxyType
from typing import cast
from unittest import mock

import pytest
from starlette.datastructures import QueryParams
from starlette.requests import Request

from domain.common.repository.entities import PolicyEntity
from domain.common.service.exceptions import ServiceException
from domain.execution_engine.services.execution_engine import (
    ExecutionEngineService
)


def test_validate_invalid_input_values(
    execution_engine_service: ExecutionEngineService,
    policy_json
):
    # Arrange
    execution_engine_service._config_backend_repository.read_policy = mock.Mock(    # noqa
        return_value=PolicyEntity(**policy_json)
    )

    # Assert
    with pytest.raises(ServiceException) as e:
        execution_engine_service.validate_input_values(
            policy_id=policy_json["id"],
            input_values=QueryParams(MappingProxyType(
                {"invalid_variable_name": "any_value"}
            )),
        )
    assert e.value.additional_content == "input_values_does_not_match_policy"


def test_validate_valid_input_values(
    execution_engine_service: ExecutionEngineService,
    policy_json
):
    # Arrange
    execution_engine_service._config_backend_repository.read_policy = mock.Mock(    # noqa
        return_value=PolicyEntity(**policy_json)
    )

    # Assert
    with does_not_raise_exception():
        execution_engine_service.validate_input_values(
            policy_id=policy_json["id"],
            input_values=QueryParams(MappingProxyType(
                {"age": "any_value"}
            )),
        )


@pytest.mark.asyncio
async def test_policy_evaluation(
    execution_engine_service: ExecutionEngineService,
    policy_json
):
    """
        Policy evaluation is a `async_generator`,
        this test (similar to a `TableDrivenTest`) will evaluate:
            - Policy not changed.
            - Policy changed.
            - Input values does not match the policy anymore.
               (`error` event type)
    """
    # Arrange
    class StubRequest:
        is_disconected = False

        async def is_disconnected(self):
            return self.is_disconected
    stub_request = StubRequest()

    policy_entity = PolicyEntity(**policy_json)
    input_values = QueryParams(MappingProxyType({"age": 18}))

    expected_evaluations = [
        1000.0,
        0.0,
        {
            "error": "The passed query parameters' names do not"
                     " match the policy anymore. Please, try again."
        }
    ]

    # Act
    c = 0
    async for result in execution_engine_service.execute_policy(
        cast(Request, stub_request),
        policy_entity,
        input_values
    ):
        # Input values does not match the policy anymore. (`error` event type)
        if c == 2:
            assert result.event == "error"
            assert json.loads(result.data) == expected_evaluations[c]
        # Policy changed.
        elif c == 1:
            assert (
                json.loads(result.data)["decision"] == expected_evaluations[c]
            )
            execution_engine_service._stream_execution_engine_queue.put_nowait(
                policy_entity.id
            )
            policy_json_to_update = deepcopy(policy_json)
            policy_json_to_update["policy_flow"]["block_targets"][0]["variable_name"] = "invalid" # noqa
            execution_engine_service._config_backend_repository.read_policy = mock.Mock(    # noqa
                return_value=PolicyEntity(**policy_json_to_update)
            )
        # Policy not changed.
        else:
            assert (
                json.loads(result.data)["decision"] == expected_evaluations[c]
            )
            execution_engine_service._stream_execution_engine_queue.put_nowait(
                policy_entity.id
            )
            policy_json_to_update = deepcopy(policy_json)
            policy_json_to_update["policy_flow"]["block_targets"][0]["variable_operator"] = "<" # noqa
            execution_engine_service._config_backend_repository.read_policy = mock.Mock(    # noqa
                return_value=PolicyEntity(**policy_json_to_update)
            )
        c += 1
