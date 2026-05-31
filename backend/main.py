from fastapi import FastAPI
from api import main_router
from core.lifespan import lifespan
from core.logger import configure_logging

 
configure_logging()

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

