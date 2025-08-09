from fastapi import APIRouter
from api.v1.endpoints.monitoring import healthCheck
from api.v1.endpoints.upload import content

api_router = APIRouter()

api_router.include_router(healthCheck.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(content.router, prefix="/deployment", tags=["deployment"])
