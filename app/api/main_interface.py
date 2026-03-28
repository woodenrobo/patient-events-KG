from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.main_interface_service import (
    MainInterfaceService,
    get_main_interface_service,
)

router = APIRouter()


class ChatRequest(BaseModel):
    user_message: str


@router.get("/check", include_in_schema=False)
async def health_check() -> dict[str, str]:
    return {"message": "OK"}


@router.post("/chat")
async def chat_message(
    request: ChatRequest,
    service: MainInterfaceService = Depends(get_main_interface_service),
) -> str:
    return service.get_chat_response(request.user_message)
