from enum import StrEnum
from typing import LiteralString, cast

from fastapi import Depends
from neo4j import AsyncSession

from app.config.database import get_session

# --- labels & relationship types as enums so f-strings stay safe ---


class NodeLabel(StrEnum):
    PATIENT = "Patient"
    CONDITION = "Condition"
    MEDICATION = "Medication"
    SYMPTOM = "Symptom"
    CARE_EVENT = "CareEvent"
    PROVIDER = "Provider"


class RelType(StrEnum):
    HAS_CONDITION = "HAS_CONDITION"
    PRESCRIBED = "PRESCRIBED"
    EXPERIENCED = "EXPERIENCED"
    VISITED = "VISITED"
    PRECEDED_BY = "PRECEDED_BY"


_IMMUTABLE_FIELDS = {"id", "created_at"}


class MainInterfaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def merge_node(
        self,
        label: NodeLabel,
        identity_key: str,
        properties: dict,
    ) -> None:
        mutable = {k: v for k, v in properties.items() if k not in _IMMUTABLE_FIELDS}
        query = cast(
            LiteralString,
            f"""
            MERGE (n:{label} {{{identity_key}: $identity}})
            ON CREATE SET n = $all_props
            ON MATCH SET n += $mutable
            """,
        )
        await self.session.run(
            query,
            identity=properties[identity_key],
            all_props=properties,
            mutable=mutable,
        )

    async def merge_relationship(
        self,
        from_label: NodeLabel,
        from_key: str,
        from_val: str,
        rel_type: RelType,
        to_label: NodeLabel,
        to_key: str,
        to_val: str,
        rel_props: dict | None = None,
    ) -> None:
        set_clause = "SET r += $props" if rel_props else ""
        await self.session.run(
            cast(
                LiteralString,
                f"""
                MATCH (a:{from_label} {{{from_key}: $from_val}})
                MATCH (b:{to_label} {{{to_key}: $to_val}})
                MERGE (a)-[r:{rel_type}]->(b)
                {set_clause}
                """,
            ),
            from_val=from_val,
            to_val=to_val,
            props=rel_props or {},
        )

    async def get_modal_care_path(self, condition_name: str) -> list[dict]:
        result = await self.session.run(
            cast(
                LiteralString,
                """
                MATCH (p:Patient)-[:HAS_CONDITION]->(c:Condition {name: $condition})
                MATCH (p)-[:VISITED]->(e:CareEvent)
                RETURN e.name AS event, count(*) AS freq
                ORDER BY freq DESC
                """,
            ),
            condition=condition_name,
        )
        return await result.data()

    async def get_symptoms_preceding_diagnosis(self, condition_name: str) -> list[dict]:
        result = await self.session.run(
            cast(
                LiteralString,
                """
                MATCH (c:Condition {name: $condition})-[:PRECEDED_BY]->(s:Symptom)
                RETURN s.name AS symptom, count(*) AS freq
                ORDER BY freq DESC
                """,
            ),
            condition=condition_name,
        )
        return await result.data()

    async def get_medications_cooccurring_with_symptom(
        self, symptom_name: str
    ) -> list[dict]:
        result = await self.session.run(
            cast(
                LiteralString,
                """
                MATCH (p:Patient)-[:EXPERIENCED]->(s:Symptom {name: $symptom})
                MATCH (p)-[:PRESCRIBED]->(m:Medication)
                RETURN m.name AS medication, count(*) AS freq
                ORDER BY freq DESC
                """,
            ),
            symptom=symptom_name,
        )
        return await result.data()


def get_main_interface_repository(
    session: AsyncSession = Depends(get_session),
) -> MainInterfaceRepository:
    return MainInterfaceRepository(session)
