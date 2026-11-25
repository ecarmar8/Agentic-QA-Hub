from app.core.ai_provider import generate_json
from app.core.storage import add_review, add_run, audit

SYSTEM = "You are a senior software QA test design agent. Produce test design drafts. Never claim execution."

def _local(title, story, criteria, context):
    text = (story + " " + " ".join(criteria)).lower()
    cases = [
        ("TC-001", "Verify the main successful business flow", "Positive", "Valid input and authorized user", "Expected business outcome is completed and persisted", "High"),
        ("TC-002", "Verify mandatory field validation", "Negative", "Omit each mandatory field in turn", "A clear validation message is shown and no invalid record is saved", "High"),
        ("TC-003", "Verify boundary values", "Boundary", "Test minimum, maximum, zero and just-outside limits where applicable", "Values within limits are accepted; out-of-range values are rejected", "Medium"),
        ("TC-004", "Verify unauthorized access", "Security", "Repeat the operation with a user lacking permission", "Access is denied and no data is changed", "High"),
        ("TC-005", "Verify duplicate submission handling", "Negative", "Submit the same request twice, including a rapid repeat", "The system prevents unintended duplicate processing", "Medium"),
        ("TC-006", "Verify error recovery", "Resilience", "Simulate timeout or downstream service error", "The user receives a controlled error and retry behavior is safe", "Medium"),
    ]
    if any(k in text for k in ["payment", "transfer", "refund", "transaction"]):
        cases.append(("TC-007", "Verify transaction idempotency and reconciliation", "Integration", "Retry the same transaction reference and reconcile status", "No duplicate debit/credit occurs and final status is traceable", "Critical"))
    if any(k in text for k in ["date", "time", "timezone", "month", "billing"]):
        cases.append(("TC-008", "Verify date, time and timezone boundaries", "Boundary", "Test midnight, month-end, leap day and timezone conversion", "The business date and persisted timestamp follow the defined rule", "High"))
    scenarios = [{"id": c[0], "name": c[1], "type": c[2], "steps": c[3], "expected": c[4], "priority": c[5], "status": "Draft"} for c in cases]
    risks = ["Acceptance criteria may be incomplete or ambiguous; confirm with the product owner.",
             "Validate permissions and auditability for sensitive operations.",
             "Confirm integration failure and retry behavior with dependent systems."]
    coverage = [{"criterion": c, "covered_by": ["TC-001", "TC-002", "TC-003"]} for c in criteria] or [{"criterion": "General business flow (derived from story)", "covered_by": ["TC-001", "TC-002", "TC-003"]}]
    return {"summary": "Draft test design generated using local QA heuristics. Review applicability before execution.",
            "scenarios": scenarios, "risks": risks, "coverage": coverage,
            "gaps": ["Confirm exact field rules, roles, error messages and data retention requirements.",
                     "Add product-specific boundary values and integration contracts."]}

def design(req):
    def fallback():
        return _local(req.title, req.story, req.acceptance_criteria, req.context)
    prompt = {"title": req.title, "story": req.story, "acceptance_criteria": req.acceptance_criteria, "context": req.context}
    result = generate_json(SYSTEM, str(prompt) + "\nCreate summary, scenarios, risks, coverage, gaps.", fallback)
    run = add_run("Test Designer", req.title, result)
    for case in result.get("scenarios", []):
        add_review("Test Designer", case.get("name", "Test case"), case)
    audit("test_design_generated", details={"run_id": run["id"], "scenario_count": len(result.get("scenarios", []))})
    return {"run": run, "result": result}
