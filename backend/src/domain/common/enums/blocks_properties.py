from enum import Enum
from typing import Callable
from operator import eq, lt, gt, ge, le


class PolicyBlockTypesEnum(str, Enum):
    start = "start"
    condition = "condition"
    end = "end"


class PolicyBlockConditionOperatorsToPythonOperatorEnum(Enum):
    less_than = lt
    less_than_equal = le
    greater_than_equal = ge
    greater_than = gt
    equal_to = eq


class PolicyBlockConditionOperatorsEnum(str, Enum):
    less_than = "<"
    less_than_equal = "<="
    greater_than_equal = ">="
    greater_than = ">"
    equal_to = "="

    def get_python_operator(self) -> Callable[[float, float], bool]:
        py_op: PolicyBlockConditionOperatorsToPythonOperatorEnum = PolicyBlockConditionOperatorsToPythonOperatorEnum.__members__[self.name] # noqa
        return py_op.value
