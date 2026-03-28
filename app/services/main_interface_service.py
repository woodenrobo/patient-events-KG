import datetime
from uuid import UUID, uuid4

from fastapi import Depends
from pydantic import BaseModel, Field

from app.repositories.main_interface_repository import (
    MainInterfaceRepository,
    get_main_interface_repository,
)


class BaseNode(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )


class NamedNode(BaseNode):
    name: str


class ConditionNode(NamedNode):
    icd_code: str | None = None


class CareEventNode(NamedNode):
    name: str
    date: str | None = None


class MainInterfaceService:
    def __init__(self, repository: MainInterfaceRepository) -> None:
        pass

    def get_chat_response(
        self,
        user_message: str,
    ) -> str:

        return user_message


def get_main_interface_service(
    repository: MainInterfaceRepository = Depends(get_main_interface_repository),
) -> MainInterfaceService:
    return MainInterfaceService(repository)
