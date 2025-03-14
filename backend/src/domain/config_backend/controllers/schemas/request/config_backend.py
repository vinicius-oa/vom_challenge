from pydantic import BaseModel, Field, model_validator

from domain.common.repository.entities import PolicyEntityPolicyFlow
from domain.config_backend.services.config_backend.validators.policy_flow.enums.blocks_properties import (  # noqa
    ConditionBlockRequiredPropertiesEnum,
    EndBlockRequiredPropertiesEnum,
    StartBlockRequiredPropertiesEnum
)


class ConfigBackendCreatePolicyRequestPolicyFlow(PolicyEntityPolicyFlow):
    """ A block in the flow. """

    @model_validator(mode="after")
    def parse_model(self):
        """
            Maintain only required properties accordingly to its block type.
        """
        block_types_required_properties_enums = (
            StartBlockRequiredPropertiesEnum,
            ConditionBlockRequiredPropertiesEnum,
            EndBlockRequiredPropertiesEnum
        )
        block_type = next(
            (
                x for x in block_types_required_properties_enums
                if x.block_type_.value == self.block_type
            )
        )
        block_required_properties = set(block_type.get_required_properties())
        not_required_properties = set(
            x for x in self.model_fields
            if not self.model_fields[x].is_required()
        )
        for not_required_property in not_required_properties.difference(block_required_properties): # noqa
            if block_type.can_delete_property(not_required_property):
                delattr(self, not_required_property)
        return self


class ConfigBackendCreatePolicyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    policy_flow: ConfigBackendCreatePolicyRequestPolicyFlow


class ConfigBackendUpdatePolicyRequest(BaseModel):
    name: str = Field(None, min_length=1, max_length=255)
    policy_flow: ConfigBackendCreatePolicyRequestPolicyFlow = Field(None)
