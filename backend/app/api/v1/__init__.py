"""API v1 router"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, agents, policies, executions, replays, evaluations, monitoring, webhooks, audit, analytics, scheduler, notifications

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(policies.router, prefix="/policies", tags=["policies"])
api_router.include_router(executions.router, prefix="/executions", tags=["executions"])
api_router.include_router(replays.router, prefix="/replays", tags=["replays"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["scheduler"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
