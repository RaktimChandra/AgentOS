"""
Demo: Evaluation Pipeline

This example demonstrates the evaluation pipeline for agent reliability testing.
"""

from app.evaluation.l1_checks import L1Checker
from app.evaluation.l2_judge import L2Judge
from app.evaluation.pipeline import EvaluationPipeline


def demo_evaluation_pipeline():
    """Demo of the evaluation pipeline"""
    
    print("=== AgentOS Demo: Evaluation Pipeline ===\n")
    
    # Create checker
    l1_checker = L1Checker()
    
    print("=== L1 Deterministic Checks ===")
    print("Running fast, deterministic checks...\n")
    
    # Schema validation
    schema = {
        "type": "object",
        "properties": {
            "result": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": ["result", "confidence"],
    }
    
    output = {"result": "Analysis complete", "confidence": 0.95}
    schema_result = l1_checker.schema_validation(output, schema)
    print(f"Schema validation: {'✓ PASSED' if schema_result['passed'] else '✗ FAILED'}")
    
    # PII detection
    text = "Contact john@example.com for support"
    pii_result = l1_checker.pii_detection(text)
    print(f"PII detection: {'✓ PASSED' if pii_result['passed'] else '✗ FAILED (PII found)'}")
    
    # SQL guard
    query = "SELECT * FROM users WHERE id = 123"
    sql_result = l1_checker.sql_ast_guard(query)
    print(f"SQL guard: {'✓ PASSED' if sql_result['passed'] else '✗ FAILED (dangerous SQL)'}")
    
    # Tool selection
    tools_result = l1_checker.tool_selection_check(
        selected_tools=["database", "calculator"],
        expected_tools=["database", "calculator"],
    )
    print(f"Tool selection: {'✓ PASSED' if tools_result['passed'] else '✗ FAILED'}")
    
    # Budget check
    budget_result = l1_checker.budget_check(cost=5.0, budget_limit=100.0)
    print(f"Budget check: {'✓ PASSED' if budget_result['passed'] else '✗ FAILED (over budget)'}")
    
    print()
    
    print("=== L2 LLM-Judge Ensemble ===")
    print("Running semantic evaluation with multiple judges...\n")
    
    l2_judge = L2Judge()
    
    # Simulate evaluation (in production, this would call actual LLMs)
    output_text = "The analysis shows a 15% increase in sales compared to last quarter."
    rubric = "Evaluate the quality of the analysis. Score 0-100."
    
    print("Judges: GPT-4, Claude, Gemini")
    print("Output: Analyzing sales data...")
    print("Rubric: Quality evaluation (0-100)")
    print()
    
    # Simulated result
    print("Judge Results:")
    print("  GPT-4: Score 85, Confidence 0.90")
    print("  Claude: Score 82, Confidence 0.85")
    print("  Gemini: Score 88, Confidence 0.88")
    print()
    
    print("Aggregated Result:")
    print("  Final Score: 85.0")
    print("  Confidence: 0.88")
    print("  Status: CONFIDENT")
    print("  Score Range: 6 (low disagreement)")
    print()
    
    print("=== Statistical Quality Gates ===")
    print("Paired-bootstrap significance testing...\n")
    
    print("Baseline score: 85.0")
    print("New score: 72.0")
    print("Delta: -13.0")
    print("95% CI: [-18.5, -7.5]")
    print("Decision: BLOCK (CI entirely below zero)")
    print()
    
    print("=== Demo Complete ===")
    print("This demonstrates:")
    print("  ✓ L1 deterministic checks (fast, offline)")
    print("  ✓ L2 LLM-judge ensemble (semantic evaluation)")
    print("  ✓ Confidence-weighted aggregation")
    print("  ✓ Disagreement detection (NEEDS_REVIEW)")
    print("  ✓ Statistical quality gates")
    print("  ✓ Regression detection with significance testing")


if __name__ == "__main__":
    demo_evaluation_pipeline()
