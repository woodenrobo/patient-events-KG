import json
from logging import getLogger
from typing import Literal

from pydantic import BaseModel

from app.libs.agents.base import BaseAgent
from app.libs.tools.query_tool import QueryTool

logger = getLogger(__name__)

QueryMethod = Literal[
    "modal_care_path",
    "symptoms_preceding_diagnosis",
    "medications_cooccurring_with_symptom",
]

ROUTING_PROMPT = """
You are a medical knowledge graph query router.
Given a user question, determine which query to run and return JSON.

Available queries:
- "modal_care_path": requires {"arg": "<condition name>"}
- "symptoms_preceding_diagnosis": requires {"arg": "<condition name>"}
- "medications_cooccurring_with_symptom": requires {"arg": "<symptom name>"}

Return: {"method": "<query name>", "arg": "<value>"}
""".strip()

NARRATION_PROMPT = """
You are a medical assistant. Given a JSON list of query results, write a clear,
concise natural language summary for a clinician.

Return: {"response": "<summary>"}
""".strip()


class QueryRouting(BaseModel):
    method: QueryMethod
    arg: str


class NarrationResult(BaseModel):
    response: str


class QueryAgent(BaseAgent):
    def __init__(self, query_tool: QueryTool) -> None:
        self.query_tool = query_tool

    async def run(self, user_message: str) -> str:
        routing = await self.complete(ROUTING_PROMPT, user_message, QueryRouting)
        results = await getattr(self.query_tool, routing.method)(routing.arg)
        logger.info("QueryAgent results %s", results)
        narration = await self.complete(
            NARRATION_PROMPT, json.dumps(results), NarrationResult
        )
        logger.info("QueryAgent narration %s", narration)
        return narration.response
