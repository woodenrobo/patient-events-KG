import datetime
from typing import Annotated, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.repositories.main_interface_repository import NodeLabel


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


class PatientNode(NamedNode):
    label: Literal[NodeLabel.PATIENT] = NodeLabel.PATIENT


class ConditionNode(NamedNode):
    label: Literal[NodeLabel.CONDITION] = NodeLabel.CONDITION
    icd_code: str | None = None


class MedicationNode(NamedNode):
    label: Literal[NodeLabel.MEDICATION] = NodeLabel.MEDICATION


class SymptomNode(NamedNode):
    label: Literal[NodeLabel.SYMPTOM] = NodeLabel.SYMPTOM


class CareEventNode(NamedNode):
    label: Literal[NodeLabel.CARE_EVENT] = NodeLabel.CARE_EVENT
    date: str | None = None


class ProviderNode(NamedNode):
    label: Literal[NodeLabel.PROVIDER] = NodeLabel.PROVIDER


AnyNode = Annotated[
    PatientNode
    | ConditionNode
    | MedicationNode
    | SymptomNode
    | CareEventNode
    | ProviderNode,
    Field(discriminator="label"),
]
