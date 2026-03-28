from collections.abc import AsyncGenerator
from functools import lru_cache

from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession

from app.config.environment import settings


@lru_cache(maxsize=1)
def get_driver() -> AsyncDriver:
    return AsyncGraphDatabase.driver(
        settings.neo4j_uri,
        auth=(
            settings.neo4j_username,
            settings.neo4j_password.get_secret_value(),
        ),
    )


async def verify_database_connectivity() -> None:
    await get_driver().verify_connectivity()


async def close_database_driver() -> None:
    await get_driver().close()
    get_driver.cache_clear()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_driver().session(database=settings.neo4j_database) as session:
        yield session
