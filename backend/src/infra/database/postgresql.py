from infra.database.base import DatabaseABC


class PostgreSQLDatabase(DatabaseABC):
    def __init__(self, **kwargs):
        raise NotImplementedError

    def setup_database(self):
        raise NotImplementedError

    def get_connection(self):
        raise NotImplementedError
