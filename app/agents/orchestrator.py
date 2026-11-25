from app.agents.test_designer import design
from app.agents.failure_analyzer import analyze
from app.agents.evidence_generator import generate

def run_workflow(design_request=None, failure_request=None, evidence_request=None):
    output = {}
    if design_request:
        output["test_design"] = design(design_request)
    if failure_request:
        output["failure_analysis"] = analyze(failure_request)
    if evidence_request:
        output["evidence"] = generate(evidence_request)
    return output
