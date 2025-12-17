"""UI-level utilities for CareerLens.

Keep UI concerns (like locating bundled assets) centralized here to avoid
duplicated path/IO logic across components.
"""

from __future__ import annotations

import base64
import os
from typing import Iterable, Optional


def _workspace_root() -> str:
    """Return the repository/workspace root (parent of the `ui/` package)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _candidate_asset_dirs() -> list[str]:
    """Directories to search for UI assets.

    Order matters: CWD first (supports running from different entrypoints),
    then workspace root (where assets are stored in this repo).
    """
    dirs = []
    try:
        dirs.append(os.getcwd())
    except Exception:
        pass

    root = _workspace_root()
    if root not in dirs:
        dirs.append(root)

    return dirs


def get_logo_path(
    *,
    override_name: str = "logo.png",
    default_name: str = "CareerLens_Logo.png",
    search_dirs: Optional[Iterable[str]] = None,
) -> Optional[str]:
    """Resolve the logo image path.

    Precedence:
    - If an override file exists (e.g. `logo.png`), use it.
    - Otherwise fall back to the default bundled logo.

    Returns None if no logo file is found.
    """
    dirs = list(search_dirs) if search_dirs is not None else _candidate_asset_dirs()

    # 1) Override wins across all candidate dirs
    for d in dirs:
        candidate = os.path.join(d, override_name)
        if os.path.exists(candidate):
            return candidate

    # 2) Default logo
    for d in dirs:
        candidate = os.path.join(d, default_name)
        if os.path.exists(candidate):
            return candidate

    return None


def get_logo_base64(
    *,
    override_name: str = "logo.png",
    default_name: str = "CareerLens_Logo.png",
    search_dirs: Optional[Iterable[str]] = None,
) -> Optional[str]:
    """Return the logo file encoded as Base64, or None if missing/unreadable."""
    logo_path = get_logo_path(
        override_name=override_name,
        default_name=default_name,
        search_dirs=search_dirs,
    )
    if not logo_path:
        return None

    try:
        with open(logo_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception:
        return None
