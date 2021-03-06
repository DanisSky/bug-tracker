from fastapi import APIRouter

from api.api_v1.endpoints import users, login, managers, tasks

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(managers.router, prefix="/users/control", tags=["managers"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
