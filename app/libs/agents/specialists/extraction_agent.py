from logging import getLogger
from string import Template

from pydantic import BaseModel

from app.libs.agents.base import BaseAgent
from app.libs.tools.ingestion_tool import IngestionTool
from app.models.nodes import AnyNode
from app.repositories.main_interface_repository import RelType

logger = getLogger(__name__)

NodeOutput = AnyNode


class RelationshipOutput(BaseModel):
    from_label: str
    from_key: str
    from_val: str
    type: RelType
    to_label: str
    to_key: str
    to_val: str


class ExtractionResult(BaseModel):
    nodes: list[NodeOutput]
    relationships: list[RelationshipOutput]


EXTRACTION_PROMPT = (
    Template("""
You are a medical entity extractor. Given a patient message, extract all entities and relationships.

Return JSON with this shape:
{
  "nodes": [
    {"label": "$patient_label", "name": "..."},
    {"label": "$condition_label", "name": "...", "icd_code": "..."},
    {"label": "$medication_label", "name": "..."},
    {"label": "$symptom_label", "name": "..."},
    {"label": "$care_event_label", "name": "...", "date": "..."},
    {"label": "$provider_label", "name": "..."}
  ],
  "relationships": [
    {"from_label": "...", "from_key": "name", "from_val": "...",
     "type": $rel_types,
     "to_label": "...", "to_key": "name", "to_val": "..."}
  ]
}

Only include nodes and relationships present in the message. Omit optional fields if unknown.
""")
    .substitute(
        patient_label="Patient",
        condition_label="Condition",
        medication_label="Medication",
        symptom_label="Symptom",
        care_event_label="CareEvent",
        provider_label="Provider",
        rel_types=" | ".join(RelType),
    )
    .strip()
)


class ExtractionAgent(BaseAgent):
    def __init__(self, ingestion_tool: IngestionTool) -> None:
        self.ingestion_tool = ingestion_tool

    async def run(self, user_message: str) -> None:
        result = await self.complete(EXTRACTION_PROMPT, user_message, ExtractionResult)
        logger.info("ExtractionAgent result %s", result)

        for node in result.nodes:
            await self.ingestion_tool.ingest_node(node)

        for rel in result.relationships:
            await self.ingestion_tool.ingest_relationship(
                rel.from_label,
                rel.from_key,
                rel.from_val,
                rel.type,
                rel.to_label,
                rel.to_key,
                rel.to_val,
            )
