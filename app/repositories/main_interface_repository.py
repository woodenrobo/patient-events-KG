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


class MainInterfaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def merge_node(
        self,
        label: NodeLabel,
        identity_key: str,
        properties: dict,
    ) -> None:
        """MERGE a node on identity_key, then SET all properties."""
        query = cast(
            LiteralString,
            f"MERGE (n:{label} {{{identity_key}: $identity}}) SET n += $props",
        )
        await self.session.run(
            query,
            identity=properties[identity_key],
            props=properties,
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
        """MERGE a relationship between two existing nodes."""
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


def get_main_interface_repository(
    session: AsyncSession = Depends(get_session),
) -> MainInterfaceRepository:
    return MainInterfaceRepository(session)
