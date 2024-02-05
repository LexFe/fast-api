from fastapi import APIRouter

from app.routers.endpoints.auth import router as auth_router
from app.routers.endpoints.user import router as user_router

routers = APIRouter()
router_list = [auth_router,user_router]

for router in router_list:
    routers.include_router(router)