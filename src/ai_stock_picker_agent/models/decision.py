from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field

from .common import ExperimentMeta, ExpectedReturnRange, TimeHorizon


class RejectionReason(BaseModel):
    ticker: str = Field(..., description="Rejected company ticker.")
    reason: str = Field(..., description="Primary reason this company was not selected.")


class RiskItem(BaseModel):
    risk: str = Field(..., description="Description of the risk.")
    invalidation_signal: str = Field(..., description="Observable signal that would invalidate the thesis.")


class PickBestCompanyOutput(BaseModel):
    """
    Output schema for pick_best_company task (investment committee memo).
    """
    meta: ExperimentMeta

    selected_company: str = Field(..., description="Name of the selected company.")
    ticker: str = Field(..., description="Ticker of the selected company.")

    time_horizon: TimeHorizon = Field(..., description="Primary holding horizon for the recommendation.")
    expected_return_range: ExpectedReturnRange = Field(..., description="Expected return range over the time_horizon.")

    investment_thesis: str = Field(..., description="3–6 sentence investment thesis.")
    key_assumptions: List[str] = Field(..., min_items=1, description="Core assumptions underlying the thesis.")
    key_risks: List[RiskItem] = Field(..., min_items=1, description="Major risks and early failure signals.")

    disagreement_notes: Optional[str] = Field(
        default=None,
        description="What made the decision hard / debated trade-offs / key uncertainties."
    )

    rejected_companies: List[RejectionReason] = Field(..., description="Why each other candidate was rejected.")
    confidence_level: int = Field(..., ge=1, le=5, description="Overall confidence (1=low, 5=high).")

    sources: List[str] = Field(..., min_items=1, description="Sources used to support the decision (URLs, doc IDs, etc.).")
