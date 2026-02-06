import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from src.core import setup_logging
from src.database import init_db
from src.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger("URL Shortener")

    logger.info("Application startup")

    try:
        init_db()
        logger.info("Database initialized")
    except Exception:
        logger.exception("Failed to initialize database")
        raise

    yield

    logger.info("Application shutdown")


app = FastAPI(
    title="URL Shortener",
    lifespan=lifespan,
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
