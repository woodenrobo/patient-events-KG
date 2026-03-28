from fastapi import Depends
from neo4j import Session

from app.config.database import get_session


class MainInterfaceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session


def get_main_interface_repository(
    session=Depends(get_session),
) -> MainInterfaceRepository:
    return MainInterfaceRepository(session)
