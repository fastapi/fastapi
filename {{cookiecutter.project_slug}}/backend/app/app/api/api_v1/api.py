from fastapi import APIRouter

from app.api.api_v1.endpoints.role import router as roles_router
from app.api.api_v1.endpoints.token import router as token_router
from app.api.api_v1.endpoints.user import router as user_router
from app.api.api_v1.endpoints.utils import router as utils_router

api_router = APIRouter()
api_router.include_router(roles_router)
api_router.include_router(token_router)
api_router.include_router(user_router)
api_router.include_router(utils_router)
