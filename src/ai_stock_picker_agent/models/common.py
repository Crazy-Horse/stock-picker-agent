from __future__ import annotations

from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class ConfidenceInterval(BaseModel):
    low: float = Field(..., ge=0, le=5)
    high: float = Field(..., ge=0, le=5)

    def is_valid(self) -> bool:
        return self.low <= self.high

class ExperimentMeta(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"run_{datetime.now().strftime('%Y%m%d_%H%M')}")
    timestamp: datetime = Field(default_factory=datetime.now)
    model_name: str = "gpt-4o"

class ExpectedReturnRange(BaseModel):
    bull_case_pct: float = Field(..., description="Annualized upside potential")
    bear_case_pct: float = Field(..., description="Annualized downside risk")
    base_case_pct: float = Field(..., description="Expected annualized return")

class TimeHorizon(BaseModel):
    period: str = Field(..., description="e.g., '12-18 months'")
    conviction: int = Field(..., ge=1, le=5)