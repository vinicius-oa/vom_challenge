from enum import Enum
from typing import Generator, Type, TypeVar

from domain.common.enums.blocks_properties import PolicyBlockTypesEnum

BlockRequiredPropertiesEnum = TypeVar(
    'BlockRequiredPropertiesEnum',
    bound=Enum
)


class CommonBlockRequiredPropertiesMethods:

    @classmethod
    def get_required_properties(
        cls: Type[BlockRequiredPropertiesEnum]
    ) -> Generator:
        return (
            x.value for x in cls.__members__.values()
            if not isinstance(x.value, Enum) and not isinstance(x.value, tuple)
        )

    @classmethod
    def can_delete_property(
        cls: Type[BlockRequiredPropertiesEnum],
        property_name: str
    ) -> bool:
        if not hasattr(cls, "list_not_del_properties"):
            return True
        return property_name not in cls.list_not_del_properties.value


class StartBlockRequiredPropertiesEnum(
    CommonBlockRequiredPropertiesMethods,
    Enum
):
    block_type_ = PolicyBlockTypesEnum.start
    block_targets = "block_targets"


class ConditionBlockRequiredPropertiesEnum(
    CommonBlockRequiredPropertiesMethods,
    Enum
):
    block_type_ = PolicyBlockTypesEnum.condition
    variable_operator = "variable_operator"
    variable_name = "variable_name"
    variable_value = "variable_value"
    block_targets = "block_targets"
    list_not_del_properties = "flow",


class EndBlockRequiredPropertiesEnum(
    CommonBlockRequiredPropertiesMethods,
    Enum
):
    block_type_ = PolicyBlockTypesEnum.end
    flow = "flow"
    output = "output"
