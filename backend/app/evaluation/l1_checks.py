"""L1 deterministic checks for evaluation"""

import json
import re
from typing import Dict, Any, List, Optional
from jsonschema import validate, ValidationError


class L1Checker:
    """L1 deterministic checks for agent evaluation"""
    
    @staticmethod
    def schema_validation(output: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate output against JSON schema
        
        Args:
            output: Output to validate
            schema: JSON schema
            
        Returns:
            Validation result
        """
        try:
            validate(instance=output, schema=schema)
            return {
                "check": "schema_validation",
                "passed": True,
                "error": None,
            }
        except ValidationError as e:
            return {
                "check": "schema_validation",
                "passed": False,
                "error": str(e),
            }
    
    @staticmethod
    def citation_check(output: str, citations: List[str]) -> Dict[str, Any]:
        """
        Check if citations are present and valid
        
        Args:
            output: Output text
            citations: Expected citations
            
        Returns:
            Citation check result
        """
        missing_citations = []
        
        for citation in citations:
            if citation not in output:
                missing_citations.append(citation)
        
        return {
            "check": "citation_check",
            "passed": len(missing_citations) == 0,
            "missing_citations": missing_citations,
            "citation_count": len(citations),
            "found_count": len(citations) - len(missing_citations),
        }
    
    @staticmethod
    def sql_ast_guard(query: str) -> Dict[str, Any]:
        """
        Guard against dangerous SQL patterns
        
        Args:
            query: SQL query
            
        Returns:
            SQL guard result
        """
        dangerous_patterns = [
            r"DROP\s+TABLE",
            r"DELETE\s+FROM",
            r"TRUNCATE",
            r"ALTER\s+TABLE",
            r"GRANT\s+",
            r"REVOKE\s+",
        ]
        
        violations = []
        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                violations.append(pattern)
        
        return {
            "check": "sql_ast_guard",
            "passed": len(violations) == 0,
            "violations": violations,
        }
    
    @staticmethod
    def pii_detection(text: str) -> Dict[str, Any]:
        """
        Detect PII in text
        
        Args:
            text: Text to check
            
        Returns:
            PII detection result
        """
        pii_patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        }
        
        detected_pii = []
        
        for pii_type, pattern in pii_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                detected_pii.append({
                    "type": pii_type,
                    "matched_text": match.group(),
                    "position": match.start(),
                })
        
        return {
            "check": "pii_detection",
            "passed": len(detected_pii) == 0,
            "detected_pii": detected_pii,
        }
    
    @staticmethod
    def tool_selection_check(
        selected_tools: List[str],
        expected_tools: List[str],
    ) -> Dict[str, Any]:
        """
        Check if correct tools were selected
        
        Args:
            selected_tools: Tools selected by agent
            expected_tools: Expected tools
            
        Returns:
            Tool selection check result
        """
        missing_tools = set(expected_tools) - set(selected_tools)
        extra_tools = set(selected_tools) - set(expected_tools)
        
        return {
            "check": "tool_selection",
            "passed": len(missing_tools) == 0 and len(extra_tools) == 0,
            "missing_tools": list(missing_tools),
            "extra_tools": list(extra_tools),
            "correct_count": len(set(selected_tools) & set(expected_tools)),
        }
    
    @staticmethod
    def trajectory_check(
        actual_trajectory: List[str],
        expected_trajectory: List[str],
    ) -> Dict[str, Any]:
        """
        Check if execution trajectory matches expected
        
        Args:
            actual_trajectory: Actual execution path
            expected_trajectory: Expected execution path
            
        Returns:
            Trajectory check result
        """
        if actual_trajectory == expected_trajectory:
            return {
                "check": "trajectory",
                "passed": True,
                "mismatch_index": None,
            }
        
        # Find first mismatch
        for i, (actual, expected) in enumerate(zip(actual_trajectory, expected_trajectory)):
            if actual != expected:
                return {
                    "check": "trajectory",
                    "passed": False,
                    "mismatch_index": i,
                    "expected": expected,
                    "actual": actual,
                }
        
        return {
            "check": "trajectory",
            "passed": False,
            "mismatch_index": min(len(actual_trajectory), len(expected_trajectory)),
            "reason": "Length mismatch",
        }
    
    @staticmethod
    def budget_check(
        cost: float,
        budget_limit: float,
    ) -> Dict[str, Any]:
        """
        Check if execution is within budget
        
        Args:
            cost: Actual cost
            budget_limit: Budget limit
            
        Returns:
            Budget check result
        """
        return {
            "check": "budget",
            "passed": cost <= budget_limit,
            "cost": cost,
            "budget_limit": budget_limit,
            "overage": max(0, cost - budget_limit),
        }
    
    @staticmethod
    def latency_check(
        latency_ms: float,
        max_latency_ms: float,
    ) -> Dict[str, Any]:
        """
        Check if latency is within limits
        
        Args:
            latency_ms: Actual latency
            max_latency_ms: Maximum allowed latency
            
        Returns:
            Latency check result
        """
        return {
            "check": "latency",
            "passed": latency_ms <= max_latency_ms,
            "latency_ms": latency_ms,
            "max_latency_ms": max_latency_ms,
            "overage_ms": max(0, latency_ms - max_latency_ms),
        }
    
    @classmethod
    def run_all_l1_checks(
        cls,
        output: Any,
        checks_config: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Run all configured L1 checks
        
        Args:
            output: Agent output
            checks_config: Configuration for which checks to run
            
        Returns:
            List of check results
        """
        results = []
        
        if "schema" in checks_config:
            results.append(cls.schema_validation(output, checks_config["schema"]))
        
        if "citations" in checks_config:
            if isinstance(output, str):
                results.append(cls.citation_check(output, checks_config["citations"]))
        
        if "sql_query" in checks_config:
            results.append(cls.sql_ast_guard(checks_config["sql_query"]))
        
        if "text" in checks_config:
            results.append(cls.pii_detection(checks_config["text"]))
        
        if "tools" in checks_config:
            results.append(cls.tool_selection_check(
                checks_config["tools"]["selected"],
                checks_config["tools"]["expected"],
            ))
        
        if "trajectory" in checks_config:
            results.append(cls.trajectory_check(
                checks_config["trajectory"]["actual"],
                checks_config["trajectory"]["expected"],
            ))
        
        if "cost" in checks_config:
            results.append(cls.budget_check(
                checks_config["cost"]["actual"],
                checks_config["cost"]["limit"],
            ))
        
        if "latency" in checks_config:
            results.append(cls.latency_check(
                checks_config["latency"]["actual"],
                checks_config["latency"]["limit"],
            ))
        
        return results


# Global L1 checker instance
l1_checker = L1Checker()
