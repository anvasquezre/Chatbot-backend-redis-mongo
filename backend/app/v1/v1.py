from app.v1.routers import sessions_router
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])

routers_included_in_v1 = [
    sessions_router.router,
]


for router_in_v1 in routers_included_in_v1:
    router.include_router(router_in_v1)
