from enum import Enum


class ExceptionErrorMsgs(str, Enum):
    POLICY_NOT_FOUND = "Policy does not exist."
    POLICY_ALREADY_EXISTS = "Policy name already exists."
    NOT_ONE_POLICY = "There are no policies."

    DB_POLICY_ALREADY_EXISTS = (
        "(sqlite3.IntegrityError) UNIQUE constraint failed: policies.name"
    )