"""L2 LLM-judge ensemble for evaluation"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class L2Judge:
    """LLM-judge ensemble for semantic evaluation"""
    
    def __init__(self):
        self.judges = {
            "gpt4": self._gpt4_judge,
            "claude": self._claude_judge,
            "gemini": self._gemini_judge,
        }
        self.cache = {}
    
    async def evaluate(
        self,
        output: str,
        rubric: str,
        reference: Optional[str] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """
        Evaluate output using judge ensemble
        
        Args:
            output: Output to evaluate
            rubric: Evaluation rubric
            reference: Optional reference output
            use_cache: Whether to use cached results
            
        Returns:
            Evaluation result
        """
        # Check cache
        cache_key = self._cache_key(output, rubric, reference)
        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]
        
        # Run all judges in parallel
        judge_results = await asyncio.gather(
            *[
                judge(output, rubric, reference)
                for judge in self.judges.values()
            ],
            return_exceptions=True,
        )
        
        # Process results
        valid_results = []
        for i, result in enumerate(judge_results):
            if isinstance(result, Exception):
                print(f"Judge {list(self.judges.keys())[i]} failed: {result}")
            else:
                valid_results.append(result)
        
        # Aggregate results
        aggregated = self._aggregate_results(valid_results)
        
        # Cache result
        if use_cache:
            self.cache[cache_key] = aggregated
        
        return aggregated
    
    async def _gpt4_judge(
        self,
        output: str,
        rubric: str,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """GPT-4 judge"""
        # In production, this would call OpenAI API
        # For now, return a simulated result
        return {
            "judge": "gpt4",
            "score": 85,
            "confidence": 0.9,
            "reasoning": "Output meets most criteria in rubric",
        }
    
    async def _claude_judge(
        self,
        output: str,
        rubric: str,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Claude judge"""
        # In production, this would call Anthropic API
        return {
            "judge": "claude",
            "score": 82,
            "confidence": 0.85,
            "reasoning": "Good quality output with minor issues",
        }
    
    async def _gemini_judge(
        self,
        output: str,
        rubric: str,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Gemini judge"""
        # In production, this would call Google API
        return {
            "judge": "gemini",
            "score": 88,
            "confidence": 0.88,
            "reasoning": "Strong alignment with rubric",
        }
    
    def _aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from multiple judges"""
        if not results:
            return {
                "score": 0,
                "confidence": 0,
                "status": "NO_JUDGES",
                "individual_results": [],
            }
        
        scores = [r["score"] for r in results]
        confidences = [r["confidence"] for r in results]
        
        # Calculate weighted average (confidence-weighted)
        weighted_sum = sum(s * c for s, c in zip(scores, confidences))
        total_confidence = sum(confidences)
        
        avg_score = weighted_sum / total_confidence if total_confidence > 0 else 0
        avg_confidence = sum(confidences) / len(confidences)
        
        # Check for disagreement
        score_range = max(scores) - min(scores)
        
        if score_range > 20:
            status = "NEEDS_REVIEW"
        elif score_range > 10:
            status = "LOW_CONFIDENCE"
        else:
            status = "CONFIDENT"
        
        return {
            "score": avg_score,
            "confidence": avg_confidence,
            "status": status,
            "score_range": score_range,
            "individual_results": results,
            "judge_count": len(results),
        }
    
    def _cache_key(
        self,
        output: str,
        rubric: str,
        reference: Optional[str],
    ) -> str:
        """Generate cache key"""
        import hashlib
        data = f"{output}|{rubric}|{reference or ''}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def clear_cache(self):
        """Clear evaluation cache"""
        self.cache.clear()


# Global L2 judge instance
l2_judge = L2Judge()
