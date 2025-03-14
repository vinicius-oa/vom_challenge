from enum import Enum

from domain.config_backend.enums.error_messages import (
    ExceptionErrorMsgs as ConfigBackendExceptionErrorMsgs,
)


class ExceptionErrorMsgs(str, Enum):
    POLICY_NOT_FOUND = ConfigBackendExceptionErrorMsgs.POLICY_NOT_FOUND.value

    EXECUTION_ENGINE_INVALID_TYPE_QUERY_PARAMS = (
        "Query parameters' values must be numbers."
    )
    EXECUTION_ENGINE_INVALID_QUERY_PARAMS = (
        "Passed query parameters' names "
        "do not match the policy's variables names."
    )
