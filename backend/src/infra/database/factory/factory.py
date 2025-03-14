from typing import Any, Dict, Type, TypedDict

from config import app_settings
from infra.database.base import DatabaseABC
from infra.database.factory.enums import SupportedDatabasesEnum

DatabaseParts = TypedDict(
    'DatabaseParts', {'db': Type[DatabaseABC], "kwargs": Dict[str, Any]}
)


class DatabaseFactory:
    _initializers = {}
    _app_settings = app_settings

    @classmethod
    def register(cls, db_type: SupportedDatabasesEnum):
        """ Decorator to register a database class. """
        def decorator(database_class):
            def initializer():
                if db_type == SupportedDatabasesEnum.sqlite:
                    return {
                        "db": database_class,
                        "kwargs": {"dns": cls._app_settings.DNS}
                    }
                else:
                    raise ValueError(f"Missing setup for: {database_class}")
            cls._initializers[db_type] = initializer
            return database_class

        return decorator

    @classmethod
    def get_database(cls) -> DatabaseParts:
        db_type = cls._app_settings.DATABASE
        initializer = cls._initializers.get(db_type)
        if not initializer:
            raise ValueError(f"Unsupported database type: {db_type}")

        return initializer()
