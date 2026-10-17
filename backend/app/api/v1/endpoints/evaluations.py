"""Evaluation endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.evaluation.pipeline import get_evaluation_pipeline

router = APIRouter()


class EvaluationCreate(BaseModel):
    """Evaluation request"""
    execution_id: str
    output: Any
    checks_config: Dict[str, Any]
    rubric: Optional[str] = None
    reference: Optional[str] = None


class RegressionTestRequest(BaseModel):
    """Regression test request"""
    baseline_execution_id: str
    new_execution_id: str
    baseline_output: Any
    new_output: Any
    checks_config: Dict[str, Any]
    rubric: Optional[str] = None


@router.post("/")
async def create_evaluation(
    eval_data: EvaluationCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Run evaluation on an execution"""
    pipeline = get_evaluation_pipeline(db)
    
    result = await pipeline.evaluate_execution(
        execution_id=eval_data.execution_id,
        output=eval_data.output,
        checks_config=eval_data.checks_config,
        rubric=eval_data.rubric,
        reference=eval_data.reference,
    )
    
    return result


@router.post("/regression")
async def run_regression_test(
    regression_data: RegressionTestRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Run regression test comparing two executions"""
    pipeline = get_evaluation_pipeline(db)
    
    result = await pipeline.regression_test(
        baseline_execution_id=regression_data.baseline_execution_id,
        new_execution_id=regression_data.new_execution_id,
        baseline_output=regression_data.baseline_output,
        new_output=regression_data.new_output,
        checks_config=regression_data.checks_config,
        rubric=regression_data.rubric,
    )
    
    return result


@router.post("/batch")
async def batch_evaluate(
    executions: List[Dict[str, Any]],
    checks_config: Dict[str, Any],
    rubric: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Run batch evaluation on multiple executions"""
    pipeline = get_evaluation_pipeline(db)
    
    result = await pipeline.batch_evaluate(
        executions=executions,
        checks_config=checks_config,
        rubric=rubric,
    )
    
    return result
