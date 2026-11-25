from pydantic import BaseModel, Field
from typing import Optional, Any

class TestDesignRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    story: str = Field(min_length=10, max_length=20000)
    acceptance_criteria: list[str] = []
    context: Optional[str] = Field(default="", max_length=10000)

class FailureRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    log: str = Field(min_length=5, max_length=30000)
    expected: Optional[str] = ""
    actual: Optional[str] = ""

class EvidenceRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    requirement: str = ""
    test_cases: list[dict[str, Any]] = []
    execution_results: list[dict[str, Any]] = []
    notes: str = ""

class ReviewRequest(BaseModel):
    status: str
    note: str = ""
