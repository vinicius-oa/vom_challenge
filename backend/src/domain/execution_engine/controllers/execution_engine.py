from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path
from sse_starlette import EventSourceResponse
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from config.di import DI
from config.exception import (
    GeneralException as ErrPrefix
)
from domain.common.controllers.base import BaseController
from domain.common.controllers.docs.additional_responses import (
    HTTP_500_STATUS_CODE_RESPONSE as RESPONSE_500
)
from domain.execution_engine.enums.error_messages import (
    ExceptionErrorMsgs as ErrMsg
)
from domain.execution_engine.services.execution_engine import (
    ExecutionEngineService
)


class ExecutionEngineController(BaseController):

    def __init__(self, *, router: APIRouter):
        super().__init__(router=router)

        self.router.add_api_route(
            "/policy/{id_}",
            self._execute_policy,
            methods=["GET"],
            response_class=EventSourceResponse,
            responses={
                status.HTTP_200_OK: {
                    "content": {
                        "text/event-stream": {
                            "example": {"decision": "<numerical_value>"}
                        }
                    },
                    "description": 'If a policy is changed and the current '
                                   'request do not match it anymore, '
                                   'there will be a event of type `error` '
                                   'with a JSON message in the format: '
                                   '`{"error": "<error_description>"`'
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
                status.HTTP_400_BAD_REQUEST: {
                    "content": {
                        "application/json": {
                            "example": {
                                ErrPrefix.CONTENT_PREFIX:
                                    ErrMsg.EXECUTION_ENGINE_INVALID_QUERY_PARAMS    # noqa
                            }
                        }
                    }
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "content": {
                        "application/json": {
                            "example": {
                                ErrPrefix.CONTENT_PREFIX:
                                    ErrMsg.EXECUTION_ENGINE_INVALID_TYPE_QUERY_PARAMS   # noqa
                            }
                        }
                    }
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                ErrPrefix.CONTENT_PREFIX:
                                    ErrMsg.POLICY_NOT_FOUND
                            }
                        }
                    }
                },
            }
        )

    @staticmethod
    @inject
    def _execute_policy(
        request: Request,
        id_: Annotated[int, Path(..., gt=0)],
        service: ExecutionEngineService = Depends(
            Provide[DI.execution_engine_service]
        ),
    ):
        # Validate input values i.e. must be convertible to python float objs.
        for v in request.query_params.values():
            try:
                float(v)
            except ValueError:
                return JSONResponse(
                    content={
                        ErrPrefix.CONTENT_PREFIX:
                            ErrMsg.EXECUTION_ENGINE_INVALID_TYPE_QUERY_PARAMS
                    },
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        policy = service.validate_input_values(
            policy_id=id_,
            input_values=request.query_params
        )
        return EventSourceResponse(
            service.execute_policy(request, policy, request.query_params),
        )
