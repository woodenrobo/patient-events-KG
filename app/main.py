from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main_interface import router
from app.config.database import close_database_driver, verify_database_connectivity
from app.config.environment import settings
from app.config.logging import configure_logging

configure_logging()
logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await verify_database_connectivity()
    yield
    await close_database_driver()


app = FastAPI(
    title="patient-kg",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
