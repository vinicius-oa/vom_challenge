""" Databases drivers must implement this ABC """
from abc import ABC, abstractmethod

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseABC(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def setup_database(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass
