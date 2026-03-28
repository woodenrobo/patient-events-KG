from app.libs.agents.base import BaseAgent
from app.libs.tools.query_tool import QueryTool

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


class QueryAgent(BaseAgent):
    def __init__(self, query_tool: QueryTool) -> None:
        self.query_tool = query_tool

    async def run(self, user_message: str) -> str:
        # 1. call self.complete(ROUTING_PROMPT, user_message)
        # 2. parse JSON -> {"method": ..., "arg": ...}
        # 3. call getattr(query_tool, method)(arg) -> results: list[dict]
        # 4. call self.complete(NARRATION_PROMPT, json.dumps(results))
        # 5. parse JSON -> {"response": ...}
        # 6. return response
        raise NotImplementedError
