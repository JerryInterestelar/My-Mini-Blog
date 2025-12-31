from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.models.user_model import User  # type: ignore
from app.models.post_model import Post  # type: ignore
from app.routers import user_router, auth_router, post_router, comment_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:  # type: ignore
    create_db_and_tables()
    yield


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)


@app.get('/')
async def home() -> dict[str, str]:
    return {'message': 'Go to /docs to test the API'}
