from enum import StrEnum
from logging import getLogger

from pydantic import BaseModel

from app.libs.agents.base import BaseAgent
from app.libs.agents.specialists.extraction_agent import ExtractionAgent
from app.libs.agents.specialists.query_agent import QueryAgent

logger = getLogger(__name__)


class Intent(StrEnum):
    INGEST = "INGEST"
    QUERY = "QUERY"
    BOTH = "BOTH"


ORCHESTRATOR_PROMPT = f"""
You are a medical knowledge graph router.
Given a user message, decide what action to take and return JSON.

Return: {{"intent": {" | ".join(Intent)} }}

- INGEST: message contains new patient info (symptoms, diagnoses, medications, visits)
- QUERY: message asks a question about patients or care patterns
- BOTH: message does both
""".strip()


class ClassificationResult(BaseModel):
    intent: Intent


class OrchestratorAgent(BaseAgent):
    def __init__(
        self,
        extraction_agent: ExtractionAgent,
        query_agent: QueryAgent,
    ) -> None:
        self.extraction_agent = extraction_agent
        self.query_agent = query_agent

    async def run(self, user_message: str) -> str:
        result = await self.complete(
            ORCHESTRATOR_PROMPT, user_message, ClassificationResult
        )
        logger.info("OrchestratorAgent result %s", result)

        match result.intent:
            case Intent.INGEST:
                await self.extraction_agent.run(user_message)
                return "Ingestion complete."
            case Intent.QUERY:
                return await self.query_agent.run(user_message)
            case Intent.BOTH:
                await self.extraction_agent.run(user_message)
                return await self.query_agent.run(user_message)
