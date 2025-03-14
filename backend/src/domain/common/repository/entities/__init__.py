from typing import List

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, JSON, String

from domain.common.enums.blocks_properties import (
    PolicyBlockConditionOperatorsEnum,
)
from domain.common.enums.blocks_properties import PolicyBlockTypesEnum
from infra.database.base import Base


class PolicyEntityPolicyFlow(BaseModel):
    """ A block in the flow. """
    block_type: PolicyBlockTypesEnum
    variable_operator: PolicyBlockConditionOperatorsEnum = Field(
        None,
        description=f'For blocks of type `{PolicyBlockTypesEnum.condition}`'
    )
    variable_name: str = Field(
        None,
        min_length=1,
        max_length=255,
        description=f'For blocks of type `{PolicyBlockTypesEnum.condition}`'
    )
    variable_value: float = Field(
        None,
        description=f'For blocks of type `{PolicyBlockTypesEnum.condition}`'
    )
    block_targets: List["PolicyEntityPolicyFlow"] = Field(
        None,
        description='Must be one of the following block type:'
                    f' `{PolicyBlockTypesEnum.condition}`,'
                    f' `{PolicyBlockTypesEnum.end}`, '
                    f'`{PolicyBlockTypesEnum.start}`',
        min_length=1,
        max_length=2
    )
    flow: bool = Field(
        None,
        description="Sets if the block itself must be evaluated based"
                    f" on previous `{PolicyBlockTypesEnum.condition}` result "
                    "in the policy's flow."
    )
    output: float = Field(
        None,
        description=f'For blocks of type `{PolicyBlockTypesEnum.end}`'
    )


class PolicyEntity(Base):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    policy_flow = Column(JSON, nullable=False)

    def parse_policy_flow(self) -> PolicyEntityPolicyFlow:
        return PolicyEntityPolicyFlow(**self.policy_flow)
