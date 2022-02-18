import uvicorn
from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings
from db.base import database

app = FastAPI(
    title="Bug Tracker",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
