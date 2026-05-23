from __future__ import annotations

from typing import Any

import httpx

from serpbase_mcp.config import Settings, get_settings


ENDPOINTS = {
    "search": "/google/search",
    "images": "/google/images",
    "news": "/google/news",
    "videos": "/google/videos",
    "maps_search": "/google/maps/search",
    "maps_detail": "/google/maps/detail",
}


class SerpBaseError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        http_status: int | None = None,
        api_status: int | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.api_status = api_status
        self.payload = payload or {}


class SerpBaseClient:
    def __init__(
        self,
        settings: Settings | None = None,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.transport = transport

    async def request(self, search_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        if search_type not in ENDPOINTS:
            raise ValueError(f"unknown search_type: {search_type}")
        if not self.settings.api_key:
            raise SerpBaseError(
                "SERPBASE_API_KEY is not set. Create a key at https://serpbase.dev/dashboard/api-keys and pass it in the MCP server env."
            )

        clean_payload = {key: value for key, value in payload.items() if value is not None}
        url = f"{self.settings.base_url}{ENDPOINTS[search_type]}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.settings.api_key,
            "X-SerpBase-Source": self.settings.source,
        }
        async with httpx.AsyncClient(
            timeout=self.settings.timeout,
            transport=self.transport,
        ) as client:
            response = await client.post(url, json=clean_payload, headers=headers)

        try:
            data = response.json()
        except ValueError as exc:
            raise SerpBaseError(
                f"SerpBase returned non-JSON response with HTTP {response.status_code}",
                http_status=response.status_code,
            ) from exc

        api_status = data.get("status")
        if response.status_code >= 400 or api_status not in (0, None):
            message = data.get("error") or f"SerpBase request failed with HTTP {response.status_code}"
            raise SerpBaseError(
                message,
                http_status=response.status_code,
                api_status=api_status if isinstance(api_status, int) else None,
                payload=data,
            )
        return data


def query_payload(
    query: str,
    *,
    hl: str = "en",
    gl: str = "us",
    page: int = 1,
    lat: float | None = None,
    lng: float | None = None,
    zoom: int | None = None,
) -> dict[str, Any]:
    q = str(query or "").strip()
    if not q:
        raise ValueError("query is required")
    page = int(page or 1)
    if page < 1:
        raise ValueError("page must be >= 1")
    payload: dict[str, Any] = {
        "q": q,
        "hl": (hl or "en").strip() or "en",
        "gl": (gl or "us").strip() or "us",
        "page": page,
    }
    if lat is not None or lng is not None or zoom is not None:
        if lat is None or lng is None:
            raise ValueError("lat and lng must be provided together")
        lat_value = float(lat)
        lng_value = float(lng)
        if not -90 <= lat_value <= 90:
            raise ValueError("lat must be between -90 and 90")
        if not -180 <= lng_value <= 180:
            raise ValueError("lng must be between -180 and 180")
        payload["lat"] = lat_value
        payload["lng"] = lng_value
        payload["zoom"] = int(zoom or 14)
    return payload


def maps_detail_payload(
    feature_id: str,
    *,
    hl: str = "en",
    gl: str = "us",
) -> dict[str, Any]:
    value = str(feature_id or "").strip()
    if not value:
        raise ValueError("feature_id is required")
    return {
        "feature_id": value,
        "hl": (hl or "en").strip() or "en",
        "gl": (gl or "us").strip() or "us",
    }
