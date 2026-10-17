"""API v1 router"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, agents, policies, executions, replays, evaluations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(policies.router, prefix="/policies", tags=["policies"])
api_router.include_router(executions.router, prefix="/executions", tags=["executions"])
api_router.include_router(replays.router, prefix="/replays", tags=["replays"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
