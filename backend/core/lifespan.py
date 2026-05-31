from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import engine, Base
from .celery.worker import app as celery_app

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.celery_app = celery_app
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()