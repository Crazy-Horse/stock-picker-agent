from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .common import ExperimentMeta
from .scoring import ScoreCandidatesOutput
from .decision import PickBestCompanyOutput
from ..logic.eval import consistency, citation_coverage

class Candidate(BaseModel):
    company_name: str
    ticker: str


class RetrievedDoc(BaseModel):
    """
    Minimal representation for RAG grounding.
    """
    doc_id: str = Field(..., description="Vector store ID or URL hash.")
    source: str = Field(..., description="Source name (sec, news, earnings, blog, etc.).")
    title: Optional[str] = None
    url: Optional[str] = None
    snippet: Optional[str] = None
    published_at: Optional[str] = None  # ISO string


class EvaluationMetrics(BaseModel):
    """
    Metrics computed post-run for quality control.
    """
    consistency: float = Field(..., ge=0.0, le=1.0, description="Internal consistency score (0–1).")
    citation_coverage: float = Field(..., ge=0.0, le=1.0, description="Fraction of rationale lines containing citations.")
    notes: Optional[str] = None


class StockPickerState(BaseModel):
    """
    LangGraph state for the end-to-end workflow.
    """
    meta: ExperimentMeta

    # Inputs
    query: str = Field(..., description="User query or screening objective.")
    universe: Optional[str] = Field(default=None, description="Universe definition (e.g., S&P 500, NASDAQ 100).")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Strategy constraints (sector, market cap, etc.).")

    # Intermediate artifacts
    candidates: List[Candidate] = Field(default_factory=list)
    retrieved_docs: Dict[str, List[RetrievedDoc]] = Field(default_factory=dict, description="ticker -> docs")

    scored: Optional[ScoreCandidatesOutput] = None
    decision: Optional[PickBestCompanyOutput] = None

    # Outputs / eval
    ranking: List[str] = Field(default_factory=list, description="Ordered tickers best->worst after tie-break.")
    metrics: Optional[EvaluationMetrics] = None

    # Debug/trace (keep light—don’t dump full prompts)
    debug: Dict[str, Any] = Field(default_factory=dict)
    
    def compute_metrics(scored_out):
        return EvaluationMetrics(
            consistency=consistency(scored_out),
            citation_coverage=citation_coverage(scored_out),
            notes=None
        )
