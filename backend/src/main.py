
import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.db import init_db
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    init_db()
    yield
    # after app startup

app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats", tags=["chats"])


API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
if( not API_KEY):
    raise NotImplementedError("API_KEY is not set in the environment variables")
@app.get("/")
def read_root():
    return {"Hello! You  Ghafar": f"World {API_KEY} DATABASE_URL {DATABASE_URL}"}