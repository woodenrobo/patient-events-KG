from app.libs.agents.base import BaseAgent
from app.libs.tools.ingestion_tool import IngestionTool

EXTRACTION_PROMPT = """
You are a medical entity extractor. Given a patient message, extract all entities and relationships.

Return JSON with this shape:
{
  "nodes": [
    {"label": "Patient|Condition|Medication|Symptom|CareEvent|Provider", "properties": {...}},
    ...
  ],
  "relationships": [
    {"from_label": "...", "from_key": "...", "from_val": "...",
     "type": "HAS_CONDITION|PRESCRIBED|EXPERIENCED|VISITED|PRECEDED_BY",
     "to_label": "...", "to_key": "...", "to_val": "..."},
    ...
  ]
}
""".strip()


class ExtractionAgent(BaseAgent):
    def __init__(self, ingestion_tool: IngestionTool) -> None:
        self.ingestion_tool = ingestion_tool

    async def run(self, user_message: str) -> None:
        # 1. call self.complete(EXTRACTION_PROMPT, user_message)
        # 2. parse JSON -> {"nodes": [...], "relationships": [...]}
        # 3. for each node: await ingestion_tool.ingest_node(label, properties)
        # 4. for each rel:  await ingestion_tool.ingest_relationship(...)
        raise NotImplementedError
