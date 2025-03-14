from enum import Enum


class SupportedDatabasesEnum(str, Enum):
    sqlite = "sqlite"
    postgresql = "postgresql"
