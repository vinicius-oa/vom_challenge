from config.exception import ExceptionErrorMsgs, GeneralException

HTTP_500_STATUS_CODE_RESPONSE = {
    "content": {
        "application/json": {
            "example": {
                GeneralException.CONTENT_PREFIX: ExceptionErrorMsgs.UNKNOWN
            }
        }
    }
}
