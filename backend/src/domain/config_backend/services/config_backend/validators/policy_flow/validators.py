from collections import Counter
from typing import TYPE_CHECKING

from starlette import status

from domain.common.enums.blocks_properties import PolicyBlockTypesEnum
from domain.config_backend.services.config_backend.validators.policy_flow.enums.blocks_properties import (  # noqa
    ConditionBlockRequiredPropertiesEnum,
    EndBlockRequiredPropertiesEnum,
)
from domain.config_backend.services.config_backend.validators.policy_flow.exceptions import (  # noqa
    PolicyFlowValidatorException
)

if TYPE_CHECKING:
    from domain.config_backend.controllers.schemas.request.config_backend import (  # noqa
        ConfigBackendCreatePolicyRequestPolicyFlow
    )
    from domain.common.repository.entities import PolicyEntityPolicyFlow


class PolicyFlowValidator:
    """
        Policy flow are made up of blocks. The first must be of type `start`,
        the second must be of type `condition`. There is also a validation on
        block's properties.
    """

    def __init__(
        self,
        policy_flow: "ConfigBackendCreatePolicyRequestPolicyFlow"
    ):
        self._policy_flow = policy_flow
        self._condition_blocks_variables_names = []
        self._validate()

    def _validate(self):
        self._validate_start_block()
        self._validate_policy_flow(
            policy_flow_after_start_position=self._policy_flow.block_targets[0]
        )
        self._validate_block_variable_name_property()

    def _validate_block_variable_name_property(self):
        """
            `condition` blocks cannot have the
            same value at property `variable_name`
        """
        if any(filter(
            lambda x: x > 1,
            Counter(self._condition_blocks_variables_names).values()
        )):
            raise PolicyFlowValidatorException(
                content="Blocks of type "
                        f"`{PolicyBlockTypesEnum.condition}`"
                        " are not allowed to have the same value at "
                        f"property `{ConditionBlockRequiredPropertiesEnum.variable_name.value}`"   # noqa
                ,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="variable_name_property"
            )

    def _validate_start_block(self):
        if self._policy_flow.block_type != PolicyBlockTypesEnum.start:
            raise PolicyFlowValidatorException(
                content="First block of a policy's flow must be of type "
                        f"`{PolicyBlockTypesEnum.start}`",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="start_block_1"
            )
        if len(self._policy_flow.block_targets) != 1:
            raise PolicyFlowValidatorException(
                content="property `block_targets` of block's type "
                        f"`{PolicyBlockTypesEnum.start}`"
                        " must have only one block.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="start_block_2"
            )
        if (
            self._policy_flow.block_targets[0].block_type
            != PolicyBlockTypesEnum.condition
        ):
            raise PolicyFlowValidatorException(
                content="property `block_targets` of type "
                        f"`{PolicyBlockTypesEnum.start}`"
                        " must have a block of type "
                        f"`{PolicyBlockTypesEnum.condition}`",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="start_block_3"
            )

    def _validate_policy_flow(
        self,
        *,
        policy_flow_after_start_position: "PolicyEntityPolicyFlow",
        block_position: int = 1
    ):
        """ Policy flow validation (recursively) after `start` block. """
        block = policy_flow_after_start_position
        if block.block_type == PolicyBlockTypesEnum.condition:
            self._validate_condition_block(block, block_position)

            for b in block.block_targets:
                self._validate_policy_flow(
                    policy_flow_after_start_position=b,
                    block_position=block_position + 1
                )

        elif block.block_type == PolicyBlockTypesEnum.end:
            self._validate_end_block(block)
        else:
            raise PolicyFlowValidatorException(
                content="Allowed block types for property `block_targets`"
                        f" of block type"
                        f" `{PolicyBlockTypesEnum.condition}`"
                        f": `{PolicyBlockTypesEnum.condition}` or "
                        f"`{PolicyBlockTypesEnum.end}`",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="block_targets_property"
            )

    def _validate_condition_block(
        self,
        block: "PolicyEntityPolicyFlow",
        block_position: int
    ):
        self._condition_blocks_variables_names.append(block.variable_name)
        block_must_have = (
            block.variable_operator,
            block.variable_name,
            block.variable_value,
            block.block_targets
        )
        for p in block_must_have:
            if p is None:
                err_msg = ', '.join((
                    f"'{x}'" for x
                    in ConditionBlockRequiredPropertiesEnum.get_required_properties()   # noqa
                ))
                raise PolicyFlowValidatorException(
                    content="Blocks of type "
                            f"`{PolicyBlockTypesEnum.condition}`"
                            " must have the following properties: " +
                            err_msg,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    additional_content="condition_block_required_properties"
                )
        if len(block.block_targets) != 2:
            raise PolicyFlowValidatorException(
                content="Blocks of type "
                        f"`{PolicyBlockTypesEnum.condition}`"
                        " must have 2 blocks in `block_targets` property.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="condition_block_blocks_target_property"
            )
        if block.flow is not None and block_position == 1:
            raise PolicyFlowValidatorException(
                content="Blocks of type "
                        f"`{PolicyBlockTypesEnum.condition}`"
                        " after a block type "
                        f"`{PolicyBlockTypesEnum.start}`"
                        " cannot have property `flow`",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="condition_block_flow_property"
            )
        if (
            len(set(b.flow for b in block.block_targets))
            != len(block.block_targets)
        ):
            raise PolicyFlowValidatorException(
                content="blocks in property `block_targets` cannot"
                        " have the same value at property `flow`",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                additional_content="condition_block_flow_property_value"
            )

    @staticmethod
    def _validate_end_block(block: "PolicyEntityPolicyFlow"):
        block_must_have = (
            block.flow,
            block.output,
        )
        for p in block_must_have:
            if p is None:
                err_msg = ', '.join((
                    f"'{x}'" for x in
                    EndBlockRequiredPropertiesEnum.get_required_properties()
                ))
                raise PolicyFlowValidatorException(
                    content=f"Blocks of type `{PolicyBlockTypesEnum.end}`"
                            " must have the following properties: " +
                            err_msg,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    additional_content="end_block_required_properties"
                )
