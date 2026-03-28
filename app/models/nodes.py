import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


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
