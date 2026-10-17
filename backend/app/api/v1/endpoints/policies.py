"""Policy management endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.policy.engine import policy_engine

router = APIRouter()


class PolicyCreate(BaseModel):
    """Policy creation request"""
    name: str
    description: Optional[str] = None
    rego_code: str


class PolicyResponse(BaseModel):
    """Policy response"""
    id: str
    name: str
    description: Optional[str]
    rego_code: str
    version: str
    is_active: bool


@router.post("/", response_model=PolicyResponse)
async def create_policy(
    policy_data: PolicyCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new policy"""
    import uuid
    from app.models.policy import Policy
    
    policy = Policy(
        id=str(uuid.uuid4()),
        name=policy_data.name,
        description=policy_data.description,
        rego_code=policy_data.rego_code,
    )
    
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    
    # Load policy into OPA
    await policy_engine.load_policy(
        rego_code=policy_data.rego_code,
        policy_path=policy.id,
    )
    
    return PolicyResponse(
        id=policy.id,
        name=policy.name,
        description=policy.description,
        rego_code=policy.rego_code,
        version=policy.version,
        is_active=policy.is_active,
    )


@router.get("/")
async def list_policies(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List policies"""
    from sqlalchemy import select
    from app.models.policy import Policy
    
    result = await db.execute(select(Policy))
    policies = result.scalars().all()
    
    return [
        {
            "id": policy.id,
            "name": policy.name,
            "version": policy.version,
            "is_active": policy.is_active,
        }
        for policy in policies
    ]


@router.get("/{policy_id}")
async def get_policy(
    policy_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get policy details"""
    from sqlalchemy import select
    from app.models.policy import Policy
    
    result = await db.execute(select(Policy).where(Policy.id == policy_id))
    policy = result.scalar_one_or_none()
    
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found",
        )
    
    return {
        "id": policy.id,
        "name": policy.name,
        "description": policy.description,
        "rego_code": policy.rego_code,
        "version": policy.version,
        "is_active": policy.is_active,
    }


@router.post("/{policy_id}/test")
async def test_policy(
    policy_id: str,
    input_data: dict,
    user_id: str = Depends(get_current_user_id),
):
    """Test policy against input data"""
    result = await policy_engine.evaluate(input_data)
    
    return result
