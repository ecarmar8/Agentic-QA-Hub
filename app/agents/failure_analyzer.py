from app.core.ai_provider import generate_json
from app.core.storage import add_review, add_run, audit

SYSTEM = "You are a QA failure triage assistant. Treat root causes as hypotheses and cite log clues. Do not invent facts."

def _local(title, log, expected, actual):
    low = log.lower()
    hypotheses = []
    def add(category, severity, clue, cause, next_step):
        hypotheses.append({"category": category, "severity": severity, "log_clue": clue, "possible_cause": cause, "recommended_checks": next_step, "confidence": "Medium"})
    if any(x in low for x in ["timeout", "timed out", "504", "connection refused"]):
        add("Environment / Integration", "High", "Timeout or connection failure appears in the log.", "Service unavailable, network instability, or an insufficient timeout may be involved.", "Check service health, network path, dependency latency, retry policy and correlation IDs.")
    if any(x in low for x in ["null", "undefined", "none", "keyerror", "nullpointer"]):
        add("Application / Data", "High", "Null or missing-value indicator appears in the log.", "Unexpected missing data or an unhandled null value may be involved.", "Inspect the failing payload, data setup, null handling and recent code changes.")
    if any(x in low for x in ["401", "403", "unauthorized", "forbidden", "token expired"]):
        add("Authentication / Authorization", "High", "Authorization-related status or message appears.", "Credentials, token expiry, role or permission configuration may be involved.", "Verify token validity, scopes, role mapping and test account permissions.")
    if any(x in low for x in ["assert", "expected", "actual", "assertionerror"]):
        add("Functional", "Medium", "Assertion or expected/actual mismatch appears.", "The implementation may differ from the expected business rule, or the test oracle/data may be incorrect.", "Compare requirement version, expected result, actual response and test data.")
    if any(x in low for x in ["duplicate", "unique constraint", "already exists"]):
        add("Data Integrity", "High", "Duplicate or uniqueness constraint appears.", "Duplicate submission or test-data collision may be involved.", "Check idempotency key, cleanup, uniqueness rules and parallel execution.")
    if not hypotheses:
        add("Unclassified", "Medium", "No known failure signature was detected.", "Insufficient diagnostic information to infer a likely cause.", "Collect full stack trace, timestamp, environment, build, request/correlation ID and reproducible steps.")
    return {"summary": "Triage hypotheses generated. These are not confirmed root causes.",
            "failure_type": hypotheses[0]["category"], "hypotheses": hypotheses,
            "missing_information": ["Build/version and environment", "Reproduction steps and test data identifier", "Full stack trace and correlation/request ID"],
            "recommended_priority": "High" if any(h["severity"] == "High" for h in hypotheses) else "Medium",
            "expected": expected, "actual": actual}

def analyze(req):
    def fallback():
        return _local(req.title, req.log, req.expected, req.actual)
    result = generate_json(SYSTEM, str(req.model_dump()), fallback)
    run = add_run("Failure Analyzer", req.title, result)
    add_review("Failure Analyzer", "Review failure triage: " + req.title, result)
    audit("failure_triage_generated", details={"run_id": run["id"], "hypotheses": len(result.get("hypotheses", []))})
    return {"run": run, "result": result}
