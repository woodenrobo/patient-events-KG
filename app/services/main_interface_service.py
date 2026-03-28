from fastapi import Depends

from app.repositories.main_interface_repository import (
    MainInterfaceRepository,
    get_main_interface_repository,
)


class MainInterfaceService:
    def __init__(self, repository: MainInterfaceRepository) -> None:
        pass

    def get_chat_response(
        self,
        user_message: str,
    ) -> str:

        return user_message


def get_main_interface_service(
    repository=Depends(get_main_interface_repository),
) -> MainInterfaceService:
    return MainInterfaceService(repository)
