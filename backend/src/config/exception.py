from enum import Enum
from typing import Dict, Optional


class ExceptionErrorMsgs(str, Enum):
    """ WebApp's response error messages used by all modules of it """
    UNKNOWN = "Unknown error."


class GeneralException(Exception):

    CONTENT_PREFIX = "error"

    def __init__(
        self,
        *,
        content: str,
        status_code: int,
        additional_content: Optional[str] = None
    ):
        self._content = {self.CONTENT_PREFIX: content}
        self._status_code = status_code
        self._additional_content = additional_content

    @property
    def content(self) -> Dict[str, str]:
        return self._content

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def additional_content(self) -> str:
        return self._additional_content
