from fastapi import Depends

from app.libs.agents.orchestrator import OrchestratorAgent
from app.libs.agents.specialists.extraction_agent import ExtractionAgent
from app.libs.agents.specialists.query_agent import QueryAgent
from app.libs.tools.ingestion_tool import IngestionTool
from app.libs.tools.query_tool import QueryTool
from app.repositories.main_interface_repository import (
    MainInterfaceRepository,
    get_main_interface_repository,
)


class MainInterfaceService:
    def __init__(self, repository: MainInterfaceRepository) -> None:
        ingestion_tool = IngestionTool(repository)
        query_tool = QueryTool(repository)
        extraction_agent = ExtractionAgent(ingestion_tool)
        query_agent = QueryAgent(query_tool)
        self.orchestrator = OrchestratorAgent(extraction_agent, query_agent)

    async def get_chat_response(self, user_message: str) -> str:
        return await self.orchestrator.run(user_message)


def get_main_interface_service(
    repository: MainInterfaceRepository = Depends(get_main_interface_repository),
) -> MainInterfaceService:
    return MainInterfaceService(repository)
