"""Evaluation pipeline for agent reliability testing"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.evaluation.l1_checks import l1_checker
from app.evaluation.l2_judge import l2_judge


class EvaluationPipeline:
    """Complete evaluation pipeline with L1 checks and L2 judges"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def evaluate_execution(
        self,
        execution_id: str,
        output: Any,
        checks_config: Dict[str, Any],
        rubric: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate an execution with full pipeline
        
        Args:
            execution_id: Execution identifier
            output: Agent output
            checks_config: L1 checks configuration
            rubric: L2 evaluation rubric
            reference: Reference output for comparison
            
        Returns:
            Complete evaluation result
        """
        # Run L1 checks
        l1_results = l1_checker.run_all_l1_checks(output, checks_config)
        
        # Check if all L1 checks passed
        l1_passed = all(check["passed"] for check in l1_results)
        
        # Run L2 judge if rubric provided
        l2_result = None
        if rubric and l1_passed:
            if isinstance(output, str):
                l2_result = await l2_judge.evaluate(
                    output=output,
                    rubric=rubric,
                    reference=reference,
                )
        
        # Determine overall status
        if not l1_passed:
            overall_status = "FAILED_L1"
        elif l2_result and l2_result["status"] == "NEEDS_REVIEW":
            overall_status = "NEEDS_REVIEW"
        elif l2_result and l2_result["score"] < 60:
            overall_status = "POOR_QUALITY"
        elif l2_result and l2_result["score"] < 80:
            overall_status = "ACCEPTABLE"
        else:
            overall_status = "PASSED"
        
        return {
            "execution_id": execution_id,
            "overall_status": overall_status,
            "l1_checks": l1_results,
            "l1_passed": l1_passed,
            "l2_judge": l2_result,
            "evaluated_at": datetime.utcnow().isoformat(),
        }
    
    async def regression_test(
        self,
        baseline_execution_id: str,
        new_execution_id: str,
        baseline_output: Any,
        new_output: Any,
        checks_config: Dict[str, Any],
        rubric: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run regression test comparing new execution with baseline
        
        Args:
            baseline_execution_id: Baseline execution ID
            new_execution_id: New execution ID
            baseline_output: Baseline output
            new_output: New output
            checks_config: L1 checks configuration
            rubric: L2 evaluation rubric
            
        Returns:
            Regression test result
        """
        # Evaluate baseline
        baseline_eval = await self.evaluate_execution(
            execution_id=baseline_execution_id,
            output=baseline_output,
            checks_config=checks_config,
            rubric=rubric,
        )
        
        # Evaluate new execution
        new_eval = await self.evaluate_execution(
            execution_id=new_execution_id,
            output=new_output,
            checks_config=checks_config,
            rubric=rubric,
        )
        
        # Compare results
        regression_detected = False
        regression_reasons = []
        
        # Check L1 regression
        if baseline_eval["l1_passed"] and not new_eval["l1_passed"]:
            regression_detected = True
            regression_reasons.append("L1 checks failed")
        
        # Check L2 score regression
        if baseline_eval["l2_judge"] and new_eval["l2_judge"]:
            score_delta = new_eval["l2_judge"]["score"] - baseline_eval["l2_judge"]["score"]
            if score_delta < -10:
                regression_detected = True
                regression_reasons.append(f"Score dropped by {abs(score_delta)}")
        
        # Check status regression
        if baseline_eval["overall_status"] == "PASSED" and new_eval["overall_status"] != "PASSED":
            regression_detected = True
            regression_reasons.append("Status degraded")
        
        return {
            "baseline_execution_id": baseline_execution_id,
            "new_execution_id": new_execution_id,
            "regression_detected": regression_detected,
            "regression_reasons": regression_reasons,
            "baseline_evaluation": baseline_eval,
            "new_evaluation": new_eval,
            "tested_at": datetime.utcnow().isoformat(),
        }
    
    async def batch_evaluate(
        self,
        executions: List[Dict[str, Any]],
        checks_config: Dict[str, Any],
        rubric: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate multiple executions in batch
        
        Args:
            executions: List of execution data
            checks_config: L1 checks configuration
            rubric: L2 evaluation rubric
            
        Returns:
            Batch evaluation results
        """
        results = await asyncio.gather(
            *[
                self.evaluate_execution(
                    execution_id=exec["id"],
                    output=exec["output"],
                    checks_config=checks_config,
                    rubric=rubric,
                )
                for exec in executions
            ]
        )
        
        # Aggregate statistics
        passed_count = sum(1 for r in results if r["overall_status"] == "PASSED")
        failed_count = len(results) - passed_count
        
        if results and results[0]["l2_judge"]:
            avg_score = sum(r["l2_judge"]["score"] for r in results if r["l2_judge"]) / len(results)
        else:
            avg_score = None
        
        return {
            "total_executions": len(results),
            "passed_count": passed_count,
            "failed_count": failed_count,
            "pass_rate": passed_count / len(results) if results else 0,
            "average_score": avg_score,
            "results": results,
            "evaluated_at": datetime.utcnow().isoformat(),
        }


# Global evaluation pipeline instance
def get_evaluation_pipeline(db: AsyncSession) -> EvaluationPipeline:
    """Get evaluation pipeline instance"""
    return EvaluationPipeline(db)
