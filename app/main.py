from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.config import STATIC_DIR
from app.core.storage import list_reviews, list_runs, list_audit, review_item, audit
from app.models.schemas import TestDesignRequest, FailureRequest, EvidenceRequest, ReviewRequest
from app.agents.test_designer import design
from app.agents.failure_analyzer import analyze
from app.agents.evidence_generator import generate
from app.services.reports import report_html, report_pdf, report_xlsx

app = FastAPI(title="Agentic QA Hub", version="1.0.0", description="Human-reviewed AI-assisted QA workflows")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Agentic QA Hub"}

@app.get("/api/dashboard")
def dashboard():
    reviews, runs = list_reviews(), list_runs()
    passed = failed = 0
    for r in runs:
        p = r.get("payload", {})
        passed += int(p.get("metrics", {}).get("passed", 0))
        failed += int(p.get("metrics", {}).get("failed", 0))
    return {"runs": len(runs), "reviews_pending": sum(1 for r in reviews if r["status"] == "pending"),
            "reviews_approved": sum(1 for r in reviews if r["status"] == "approved"),
            "reviews_rejected": sum(1 for r in reviews if r["status"] == "rejected"),
            "passed": passed, "failed": failed, "recent_runs": runs[:8]}

@app.post("/api/test-design")
def test_design(req: TestDesignRequest):
    return design(req)

@app.post("/api/failure-triage")
def failure_triage(req: FailureRequest):
    return analyze(req)

@app.post("/api/evidence")
def evidence(req: EvidenceRequest):
    return generate(req)

@app.get("/api/reviews")
def reviews():
    return list_reviews()

@app.post("/api/reviews/{item_id}")
def update_review(item_id: str, req: ReviewRequest):
    if req.status not in {"approved", "rejected", "pending"}:
        raise HTTPException(400, "Status must be approved, rejected or pending")
    item = review_item(item_id, req.status, req.note)
    if not item:
        raise HTTPException(404, "Review item not found")
    audit("review_updated", details={"item_id": item_id, "status": req.status})
    return item

@app.get("/api/audit")
def audit_events():
    return list_audit()

@app.get("/api/runs")
def runs():
    return list_runs()

@app.get("/api/reports/{fmt}")
def reports(fmt: str):
    reviews_data, runs_data = list_reviews(), list_runs()
    if fmt == "html":
        return HTMLResponse(report_html(reviews_data, runs_data))
    if fmt == "pdf":
        return Response(report_pdf(reviews_data, runs_data), media_type="application/pdf",
                        headers={"Content-Disposition": "attachment; filename=agentic-qa-evidence.pdf"})
    if fmt == "xlsx":
        return Response(report_xlsx(reviews_data, runs_data),
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        headers={"Content-Disposition": "attachment; filename=agentic-qa-evidence.xlsx"})
    raise HTTPException(404, "Format must be html, pdf or xlsx")
