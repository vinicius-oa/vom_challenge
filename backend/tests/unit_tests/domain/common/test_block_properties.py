import pytest

from domain.common.enums.blocks_properties import (
    PolicyBlockConditionOperatorsEnum as BlockConditionOperator,
    PolicyBlockConditionOperatorsToPythonOperatorEnum as PythonOperator
)


@pytest.mark.parametrize(
    "block_condition_operator, expected_python_operator",
    [
        (BlockConditionOperator.less_than, PythonOperator.less_than.value),
        (
            BlockConditionOperator.less_than_equal,
            PythonOperator.less_than_equal.value
        ),
        (
            BlockConditionOperator.greater_than_equal,
            PythonOperator.greater_than_equal.value
        ),
        (
            BlockConditionOperator.greater_than,
            PythonOperator.greater_than.value
        ),
        (BlockConditionOperator.equal_to, PythonOperator.equal_to.value)
    ]
)
def test_policy_block_condition_operators_enums(
    block_condition_operator: BlockConditionOperator,
    expected_python_operator
):
    assert (
        block_condition_operator.get_python_operator()
        == expected_python_operator
    )
