from app.agents.test_designer import _local
from app.agents.failure_analyzer import _local as triage
from app.agents.evidence_generator import _local as evidence
from types import SimpleNamespace

def test_test_designer_creates_scenarios():
    result = _local("Payments", "Customer makes a payment transfer", ["Payment succeeds"], "")
    assert len(result["scenarios"]) >= 6
    assert any("idempotency" in x["name"].lower() for x in result["scenarios"])

def test_failure_analyzer_marks_hypothesis():
    result = triage("API timeout", "Request timed out with HTTP 504", "", "")
    assert result["hypotheses"]
    assert "hypotheses" in result["summary"].lower() or "hypotheses" in result["summary"]

def test_evidence_counts_only_submitted_results():
    req = SimpleNamespace(execution_results=[{"status":"passed"},{"status":"failed"}],
                          requirement="", test_cases=[], notes="")
    result = evidence(req)
    assert result["metrics"]["passed"] == 1
    assert result["metrics"]["failed"] == 1
    assert result["metrics"]["pass_rate"] == 50.0
