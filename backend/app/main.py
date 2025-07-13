from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.connection import engine
from app.complaint import router
from app.complaint import models


@asynccontextmanager
async def start_db(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)
        yield
    except:
        print("Database connection failed")
        raise


app = FastAPI(lifespan=start_db)

app.include_router(router.complaint_router)