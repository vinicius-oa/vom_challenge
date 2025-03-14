from typing import Annotated, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path
from starlette import status

from config.di import DI
from config.exception import GeneralException as Err
from domain.common.controllers.base import BaseController
from domain.common.controllers.docs.additional_responses import (
    HTTP_500_STATUS_CODE_RESPONSE as RESPONSE_500
)
from domain.config_backend.controllers.schemas.request.config_backend import (
    ConfigBackendCreatePolicyRequest,
    ConfigBackendUpdatePolicyRequest
)
from domain.config_backend.controllers.schemas.response.config_backend import (
    ConfigBackendCreatePolicyResponse,
    ConfigBackendReadPolicyResponse
)
from domain.config_backend.enums.error_messages import (
    ExceptionErrorMsgs as ErrMsg
)
from domain.config_backend.services.config_backend import ConfigBackendService


class ConfigBackendController(BaseController):

    def __init__(self, *, router: APIRouter):
        super().__init__(router=router)

        self.router.add_api_route(
            "",
            self._create_policy,
            response_model=ConfigBackendCreatePolicyResponse,
            methods=["POST"],
            response_model_exclude_none=True,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "content": {
                        "application/json": {
                            "example": {
                                Err.CONTENT_PREFIX: "<error_description>"
                            }
                        }
                    },
                    "description": "It may also return the"
                                   " `Pydantic` default error format."
                },
                status.HTTP_409_CONFLICT: {
                    "content": {
                        "application/json": {
                            "example": {
                                Err.CONTENT_PREFIX:
                                    ErrMsg.POLICY_ALREADY_EXISTS
                            }
                        }
                    },
                }
            }
        )

        self.router.add_api_route(
            "/{id_}",
            self._read_policy,
            methods=["GET"],
            response_model=ConfigBackendReadPolicyResponse,
            response_model_exclude_none=True,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                Err.CONTENT_PREFIX:
                                    ErrMsg.POLICY_NOT_FOUND
                            }
                        }
                    },
                }
            }
        )

        self.router.add_api_route(
            "",
            self._read_all_policies,
            methods=["GET"],
            response_model=List[ConfigBackendReadPolicyResponse],
            response_model_exclude_none=True,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                Err.CONTENT_PREFIX:
                                    ErrMsg.NOT_ONE_POLICY
                            }
                        }
                    },
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "content": {
                        "application/json": {
                            "example": {
                              "detail": [
                                {
                                  "loc": [
                                    "string",
                                    0
                                  ],
                                  "msg": "string",
                                  "type": "string"
                                }
                              ]
                            }
                        }
                    },
                    "description": "`Pydantic` default format."
                }
            }
        )

        self.router.add_api_route(
            "/{id_}",
            self._update_policy,
            methods=["PATCH"],
            response_model=ConfigBackendReadPolicyResponse,
            response_model_exclude_none=True,
            responses={
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "content": {
                        "application/json": {
                            "example": {
                                Err.CONTENT_PREFIX: "<error_description>"
                            }
                        }
                    },
                    "description": "It may also return the"
                                   " `Pydantic` default error format."
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                Err.CONTENT_PREFIX:
                                    ErrMsg.POLICY_NOT_FOUND
                            }
                        }
                    },
                }
            }
        )

    @staticmethod
    @inject
    def _create_policy(
        payload: ConfigBackendCreatePolicyRequest,
        service: ConfigBackendService = Depends(
            Provide[DI.config_backend_service]
        ),
    ):
        return service.create_policy(payload)

    @staticmethod
    @inject
    def _read_policy(
        id_: Annotated[int, Path(..., gt=0)],
        service: ConfigBackendService = Depends(
            Provide[DI.config_backend_service]
        ),
    ):
        return service.read_policy(id_)

    @staticmethod
    @inject
    def _read_all_policies(
        service: ConfigBackendService = Depends(
            Provide[DI.config_backend_service]
        ),
    ):
        return service.read_all_policies()

    @staticmethod
    @inject
    def _update_policy(
        id_: Annotated[int, Path(..., gt=0)],
        payload: ConfigBackendUpdatePolicyRequest,
        service: ConfigBackendService = Depends(
            Provide[DI.config_backend_service]
        ),
    ):
        return service.update_policy(id_, payload)
