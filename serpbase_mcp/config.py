from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str = "https://api.serpbase.dev"
    timeout: float = 30.0
    source: str = "serpbase-mcp"


def get_settings() -> Settings:
    timeout_raw = os.getenv("SERPBASE_TIMEOUT", "30").strip()
    try:
        timeout = float(timeout_raw)
    except ValueError:
        timeout = 30.0
    if timeout <= 0:
        timeout = 30.0

    return Settings(
        api_key=os.getenv("SERPBASE_API_KEY", "").strip(),
        base_url=os.getenv("SERPBASE_BASE_URL", "https://api.serpbase.dev").rstrip("/"),
        timeout=timeout,
        source=os.getenv("SERPBASE_SOURCE", "serpbase-mcp").strip() or "serpbase-mcp",
    )
