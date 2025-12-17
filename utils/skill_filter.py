"""
Skill post-processing utilities.

Goal: Remove obvious non-skill garbage (employment type, location mode, shifts, etc.)
before persisting, comparing, or rendering "skills".
"""

from __future__ import annotations

import re
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

# Common spoken language tokens (avoid matching programming languages).
SPOKEN_LANGUAGE_TERMS = {
    "english",
    "cantonese",
    "mandarin",
    "putonghua",
    "chinese",
    "french",
    "german",
    "spanish",
    "japanese",
    "korean",
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


def looks_like_spoken_language(term: str) -> bool:
    """Heuristic to treat spoken-language requirements as non-skills.

    This prevents "English"/"Cantonese"/etc (or "fluent in English") from being
    treated as a skill for semantic matching or skill-gap displays.
    """
    if not isinstance(term, str):
        return False
    s = term.strip().lower()
    if not s:
        return False

    if s in SPOKEN_LANGUAGE_TERMS:
        return True

    # "fluent/native/proficient in <language>" variants.
    if "language" in s or "fluent" in s or "native" in s or "proficient" in s:
        return any(re.search(rf"\b{re.escape(lang)}\b", s) for lang in SPOKEN_LANGUAGE_TERMS)

    return False


def is_valid_skill(skill: str) -> bool:
    """Return True if token looks like a valid skill (not in blocklist)."""
    if not isinstance(skill, str):
        return False
    s = _canon_term(skill)
    if not s:
        return False
    if looks_like_spoken_language(s):
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

