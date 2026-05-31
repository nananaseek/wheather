from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from sqlalchemy.sql import select
from core.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

app = APIRouter()

# @app.post("/trigger-test/")
# def trigger_celery_and_db():
#     # 1. Запускаємо таску асинхронно в Celery
#     task = test_task.delay("Привіт з Celery та SQLAlchemy!")
#     return {"status": "Task sent to Celery", "task_id": task.id}


# @app.get("/check-log")
# async def read_root():
#     session: AsyncSession = AsyncSessionLocal()
#     result = select(SystemLog)
#     data = await session.execute(result)
    
#     return {"message": "Hello World", "log": data.scalars().all()}


# @app.get("/test-create")
# async def test_create():
#     session: AsyncSession = AsyncSessionLocal()
    