from typing import List, Type

from starlette import status

from config.exception import GeneralException
from domain.common.repository.entities import PolicyEntity
from domain.common.repository.exceptions import RepositoryException
from domain.config_backend.controllers.schemas.request.config_backend import (
    ConfigBackendCreatePolicyRequest,
    ConfigBackendUpdatePolicyRequest
)
from domain.config_backend.enums.error_messages import ExceptionErrorMsgs
from infra.database.base import DatabaseABC


class ConfigBackendRepository:
    def __init__(
        self,
        *,
        database: DatabaseABC,
        entity: Type[PolicyEntity],
    ):
        self._database = database
        self._entity = entity

    def create_policy(
        self,
        value: ConfigBackendCreatePolicyRequest
    ) -> PolicyEntity:
        try:
            with self._database.get_connection() as conn:
                entity = self._entity(
                    name=value.name,
                    policy_flow=value.policy_flow.model_dump(exclude_none=True)
                )
                conn.add(entity)
                conn.flush()
                conn.expunge(entity)
        except GeneralException as e:
            if (
                ExceptionErrorMsgs.DB_POLICY_ALREADY_EXISTS
                in e.additional_content
            ):
                raise RepositoryException(
                    content=ExceptionErrorMsgs.POLICY_ALREADY_EXISTS,
                    status_code=status.HTTP_409_CONFLICT,
                ) from e
            raise e
        else:
            return entity

    def read_policy(self, id_: int) -> PolicyEntity:
        with self._database.get_connection() as conn:
            entity = conn.query(
                self._entity
            ).filter(self._entity.id == id_).first()
            if entity:
                conn.expunge(entity)

        if not entity:
            raise RepositoryException(
                content=ExceptionErrorMsgs.POLICY_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return entity

    def read_all_policies(self) -> List[PolicyEntity]:
        with self._database.get_connection() as conn:
            entities = conn.query(self._entity).all()
            if entities:
                for e in entities:
                    conn.expunge(e)

        if not entities:
            raise RepositoryException(
                content=ExceptionErrorMsgs.NOT_ONE_POLICY,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return entities

    def update_policy(
        self,
        id_: int,
        value: ConfigBackendUpdatePolicyRequest
    ) -> PolicyEntity:
        with self._database.get_connection() as conn:
            entity: PolicyEntity = conn.query(
                self._entity
            ).filter(self._entity.id == id_).first()
            if entity:
                if value.name is not None:
                    entity.name = value.name
                if value.policy_flow is not None:
                    entity.policy_flow = value.policy_flow.model_dump(
                        exclude_none=True
                    )
                conn.flush()
                conn.refresh(entity)
                conn.expunge(entity)

        if not entity:
            raise RepositoryException(
                content=ExceptionErrorMsgs.POLICY_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return entity
