from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field, conint, model_validator

from .common import ConfidenceInterval, ExperimentMeta


class RubricScore(BaseModel):
    """
    Individual rubric score with supporting evidence and uncertainty.
    """
    score: conint(ge=0, le=5) = Field(..., description="Score from 0 (worst) to 5 (best).")

    confidence_interval: ConfidenceInterval = Field(
        ...,
        description="Uncertainty interval around the score (0–5 scale)."
    )

    rationale: List[str] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="1–3 concise, evidence-based bullets justifying the score. Prefer inline citations."
    )

    @model_validator(mode="after")
    def _validate_ci_contains_score(self):
        if not self.confidence_interval.is_valid():
            raise ValueError("confidence_interval must have low <= high")
        if not (self.confidence_interval.low <= float(self.score) <= self.confidence_interval.high):
            raise ValueError("score must lie within confidence_interval")
        return self


class CompanyScore(BaseModel):
    """
    Full scoring breakdown for a single company.
    """
    company_name: str = Field(..., description="Company legal or common name.")
    ticker: str = Field(..., description="Public equity ticker symbol.")

    quality: RubricScore
    growth: RubricScore
    valuation: RubricScore
    catalysts: RubricScore
    risks: RubricScore  # interpret higher = better risk posture (or define in your rubric)

    total_score: conint(ge=0, le=25) = Field(..., description="Sum of all rubric scores (0–25).")

    @model_validator(mode="after")
    def _validate_total(self):
        computed = int(self.quality.score + self.growth.score + self.valuation.score + self.catalysts.score + self.risks.score)
        if computed != int(self.total_score):
            raise ValueError(f"total_score mismatch: computed={computed} provided={self.total_score}")
        return self


class ScoreCandidatesOutput(BaseModel):
    """
    Output schema for the score_candidates task.
    """
    meta: ExperimentMeta

    methodology: str = Field(..., description="Short explanation of how scores were assigned.")
    companies: List[CompanyScore] = Field(..., min_items=1, description="List of scored companies.")
