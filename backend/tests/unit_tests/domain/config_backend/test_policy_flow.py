from contextlib import nullcontext as does_not_raise_exception
from typing import Tuple

import pytest

from domain.config_backend.services.config_backend.validators.policy_flow.enums.blocks_properties import (  # noqa
    ConditionBlockRequiredPropertiesEnum,
    EndBlockRequiredPropertiesEnum,
    StartBlockRequiredPropertiesEnum)
from domain.config_backend.services.config_backend.validators.policy_flow.exceptions import (   # noqa
    PolicyFlowValidatorException
)
from domain.config_backend.services.config_backend.validators.policy_flow.validators import (   # noqa
    PolicyFlowValidator
)


@pytest.mark.parametrize(
    "block, expected_required_properties",
    [
        (
            StartBlockRequiredPropertiesEnum, {
                StartBlockRequiredPropertiesEnum.block_targets.value
            }
        ),
        (
            EndBlockRequiredPropertiesEnum, {
                EndBlockRequiredPropertiesEnum.flow.value,
                EndBlockRequiredPropertiesEnum.output.value
            }
        ),
        (
            ConditionBlockRequiredPropertiesEnum, {
                ConditionBlockRequiredPropertiesEnum.variable_operator.value,
                ConditionBlockRequiredPropertiesEnum.variable_name.value,
                ConditionBlockRequiredPropertiesEnum.variable_value.value,
                ConditionBlockRequiredPropertiesEnum.block_targets.value
            }
        )
    ]
)
def test_block_required_properties(block, expected_required_properties):
    assert set(block.get_required_properties()) == expected_required_properties


@pytest.mark.parametrize(
    "block, block_property, expected_bool_value",
    [
        (StartBlockRequiredPropertiesEnum, "any", True),
        (EndBlockRequiredPropertiesEnum, "any", True),
        (ConditionBlockRequiredPropertiesEnum, "flow", False),
        (ConditionBlockRequiredPropertiesEnum, "any_except_flow", True)
    ]
)
def test_block_can_delete_property(block, block_property, expected_bool_value):
    assert block.can_delete_property(block_property) is expected_bool_value


def test_policy_flow_valid(valid_policy_flow):
    with does_not_raise_exception():
        PolicyFlowValidator(valid_policy_flow)


def test_policy_flow_invalid(invalid_valid_policy_flow: Tuple):
    invalid_policy_flow, expected_exception = invalid_valid_policy_flow
    with pytest.raises(PolicyFlowValidatorException) as e:
        PolicyFlowValidator(invalid_policy_flow)
    assert e.value.additional_content == expected_exception
