from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import main_router
from core.lifespan import lifespan
from core.logger import configure_logging

 
configure_logging()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

