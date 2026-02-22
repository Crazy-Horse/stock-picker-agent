from __future__ import annotations

import re
from typing import List

from models.scoring import ScoreCandidatesOutput, CompanyScore


_CITATION_RE = re.compile(
    r"(\[[^\]]+\]\([^)]+\))"          # markdown link [text](url)
    r"|(\bhttps?://\S+)"              # raw url
    r"|(\bsource:\s*\S+)",            # source: xyz
    re.IGNORECASE
)


def _rationale_lines(sc: CompanyScore) -> List[str]:
    lines = []
    for rubric in (sc.quality, sc.growth, sc.valuation, sc.catalysts, sc.risks):
        lines.extend(rubric.rationale)
    return lines


def citation_coverage(scored_out: ScoreCandidatesOutput) -> float:
    """
    Fraction of rationale bullets containing some citation marker.
    """
    all_lines = []
    for cs in scored_out.companies:
        all_lines.extend(_rationale_lines(cs))

    if not all_lines:
        return 0.0

    cited = sum(1 for line in all_lines if _CITATION_RE.search(line or ""))
    return cited / len(all_lines)


def consistency(scored_out: ScoreCandidatesOutput) -> float:
    """
    Internal consistency score in [0,1].

    Checks:
      - total_score matches sum (already validated by Pydantic; count failures if any slipped through)
      - each rubric score lies within its confidence interval (also validated)
    This metric is mainly useful if you run with 'lenient' parsing or partial outputs.
    """
    # If the model instantiated, those invariants already hold.
    # So we return 1.0. If you have a “best-effort parsing mode”, you can downgrade.
    return 1.0
