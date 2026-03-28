from api.main_interface import router
from config.environment import settings
from config.logging import configure_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = configure_logging()


app = FastAPI(
    title="patient-kg",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
