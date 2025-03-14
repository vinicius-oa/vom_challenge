import pytest

from domain.config_backend.controllers.schemas.request.config_backend import (
    ConfigBackendCreatePolicyRequestPolicyFlow
)
from . import list_invalid_policy_flow, list_valid_policy_flow_parsed


@pytest.fixture(scope="function", params=list_valid_policy_flow_parsed)
def valid_policy_flow(request):
    return request.param


@pytest.fixture(scope="function", params=list_invalid_policy_flow)
def invalid_valid_policy_flow(request):
    invalid_policy_flow = ConfigBackendCreatePolicyRequestPolicyFlow(
        **request.param["policy_flow"]
    )
    return invalid_policy_flow, request.param["expected_exception"]
