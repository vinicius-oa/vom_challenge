from pydantic import Field, model_validator

from domain.config_backend.controllers.schemas.request.config_backend import (
    ConfigBackendCreatePolicyRequest
)


class ConfigBackendCreatePolicyResponse(ConfigBackendCreatePolicyRequest):
    id: int = Field(..., gt=0)

    @model_validator(mode="after")
    def parse_model(self):
        """ Overrides parent class validator. """
        return self


class ConfigBackendReadPolicyResponse(ConfigBackendCreatePolicyResponse):
    pass
