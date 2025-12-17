"""
Skill post-processing utilities.

Goal: Remove obvious non-skill garbage (employment type, location mode, shifts, etc.)
before persisting, comparing, or rendering "skills".
"""

from __future__ import annotations

from typing import Iterable, List, Optional


# Minimal, hard blocklist: normalize to a canonical form before comparing.
NON_SKILL_TERMS = {
    "full time",
    "full-time",
    "part time",
    "part-time",
    "contract",
    "permanent",
    "temporary",
    "freelance",
    "internship",
    "remote",
    "on site",
    "onsite",
    "hybrid",
    "shift work",
    "day shift",
    "night shift",
}


def _canon_term(s: str) -> str:
    """Canonicalize a skill-ish token for equality checks."""
    x = (s or "").strip().lower()
    if not x:
        return ""
    # Unify separators and whitespace.
    x = x.replace("_", " ").replace("-", " ")
    x = " ".join(x.split())
    return x


def is_valid_skill(skill: str) -> bool:
    """Return True if token looks like a valid skill (not in blocklist)."""
    if not isinstance(skill, str):
        return False
    s = _canon_term(skill)
    if not s:
        return False
    return s not in {_canon_term(t) for t in NON_SKILL_TERMS}


def filter_skills(skills: Optional[Iterable[str]]) -> List[str]:
    """Filter + de-duplicate skills while preserving original order/casing."""
    if not skills:
        return []

    out: List[str] = []
    seen = set()
    for raw in skills:
        if not isinstance(raw, str):
            continue
        if not raw.strip():
            continue
        if not is_valid_skill(raw):
            continue

        key = _canon_term(raw)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(raw.strip())

    return out

