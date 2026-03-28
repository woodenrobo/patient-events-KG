from app.libs.agents.base import BaseAgent
from app.libs.agents.specialists.extraction_agent import ExtractionAgent
from app.libs.agents.specialists.query_agent import QueryAgent

ORCHESTRATOR_PROMPT = """
You are a medical knowledge graph router.
Given a user message, decide what action to take and return JSON.

Return: {"intent": "INGEST" | "QUERY" | "BOTH"}

- INGEST: message contains new patient info (symptoms, diagnoses, medications, visits)
- QUERY: message asks a question about patients or care patterns
- BOTH: message does both
""".strip()


class OrchestratorAgent(BaseAgent):
    def __init__(
        self,
        extraction_agent: ExtractionAgent,
        query_agent: QueryAgent,
    ) -> None:
        self.extraction_agent = extraction_agent
        self.query_agent = query_agent

    async def run(self, user_message: str) -> str:
        # 1. call self.complete(ORCHESTRATOR_PROMPT, user_message)
        # 2. parse JSON -> intent
        # 3. if INGEST or BOTH: await extraction_agent.run(user_message)
        # 4. if QUERY or BOTH:  return await query_agent.run(user_message)
        # 5. else: return "Ingestion complete."
        raise NotImplementedError
