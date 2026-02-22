from __future__ import annotations

from typing import List, Tuple
from pydantic import BaseModel

from models.scoring import CompanyScore


def _tie_break_key(cs: CompanyScore) -> Tuple:
    """
    Deterministic tie-break ordering.

    Primary: total_score (desc)
    Tie-break 1: catalysts (desc)
    Tie-break 2: valuation (desc)
    Tie-break 3: quality (desc)
    Tie-break 4: risks (desc)
    Tie-break 5: ticker (asc) for full determinism
    """
    return (
        int(cs.total_score),
        int(cs.catalysts.score),
        int(cs.valuation.score),
        int(cs.quality.score),
        int(cs.risks.score),
        cs.ticker.upper(),
    )


def rank_companies(scored: List[CompanyScore]) -> List[CompanyScore]:
    """
    Returns sorted list (best->worst) using deterministic tie-breaks.
    """
    return sorted(scored, key=_tie_break_key, reverse=True)


def pick_best(scored: List[CompanyScore]) -> CompanyScore:
    ranked = rank_companies(scored)
    if not ranked:
        raise ValueError("No scored companies to pick from.")
    return ranked[0]
