import json
import traceback
from contextlib import contextmanager
from typing import cast

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette import status

from config.exception import ExceptionErrorMsgs, GeneralException
from config.logger import logger
from infra.database.base import Base, DatabaseABC
from infra.database.factory.enums import SupportedDatabasesEnum
from infra.database.factory.factory import DatabaseFactory


@DatabaseFactory.register(SupportedDatabasesEnum.sqlite)
class SqliteDatabase(DatabaseABC):
    def __init__(self, *, dns: str):
        """
        :param dns: database connection string.
        """
        self._engine = create_engine(
            dns,
            # Every request into this WebApp creates a new thread.
            connect_args={'check_same_thread': False}
        )
        self._session_maker = sessionmaker(bind=self._engine.connect())

    def setup_database(self):
        Base.metadata.create_all(self._engine)

    @contextmanager
    def _get_database_connection(self):
        session = cast(Session, self._session_maker())
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            error = str(e) or e.__class__.__name__
            logger.error(json.dumps({
                "error": error,
                "traceback": traceback.format_exc()
            }))
            raise GeneralException(
                content=ExceptionErrorMsgs.UNKNOWN,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                additional_content=error
            ) from e
        finally:
            session.close()

    def get_connection(self):
        return self._get_database_connection()
