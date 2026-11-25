from app.core.ai_provider import generate_json
from app.core.storage import add_run, add_review, audit

SYSTEM = "You are a QA evidence reporting assistant. Summarize supplied facts only. Clearly label missing evidence."

def _local(req):
    results = req.execution_results or []
    passed = sum(1 for x in results if str(x.get("status", "")).lower() in ["pass", "passed", "approved"])
    failed = sum(1 for x in results if str(x.get("status", "")).lower() in ["fail", "failed", "blocked"])
    total = len(results)
    return {"executive_summary": f"{passed} passed, {failed} failed, {max(0,total-passed-failed)} other/outstanding out of {total} supplied execution results.",
            "requirement": req.requirement or "Not supplied",
            "test_case_count": len(req.test_cases), "execution_count": total,
            "metrics": {"passed": passed, "failed": failed, "other": max(0,total-passed-failed), "pass_rate": round((passed/total)*100, 1) if total else 0},
            "observations": ["Only supplied execution results are included; this report does not imply unprovided tests were executed."],
            "missing_evidence": ["Execution timestamp, build/version, environment and tester identity if required by your process.",
                                 "Attach screenshots, API responses or log extracts for each result where applicable."],
            "notes": req.notes}

def generate(req):
    def fallback():
        return _local(req)
    result = generate_json(SYSTEM, str(req.model_dump()), fallback)
    run = add_run("Evidence Generator", req.title, result)
    add_review("Evidence Generator", "Approve evidence report: " + req.title, result)
    audit("evidence_generated", details={"run_id": run["id"]})
    return {"run": run, "result": result}
