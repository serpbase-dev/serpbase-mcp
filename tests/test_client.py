from __future__ import annotations

import httpx
import pytest

from serpbase_mcp.client import SerpBaseClient, SerpBaseError, maps_detail_payload, query_payload
from serpbase_mcp.config import Settings


@pytest.mark.asyncio
async def test_request_posts_to_expected_endpoint_with_headers():
    seen = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["api_key"] = request.headers.get("X-API-Key")
        seen["source"] = request.headers.get("X-SerpBase-Source")
        seen["payload"] = request.read().decode()
        return httpx.Response(200, json={"status": 0, "organic": []})

    client = SerpBaseClient(
        Settings(api_key="test-key", base_url="https://api.example.test", source="pytest"),
        transport=httpx.MockTransport(handler),
    )
    data = await client.request("search", {"q": "python", "hl": "en", "gl": "us", "page": 1})

    assert data == {"status": 0, "organic": []}
    assert seen["url"] == "https://api.example.test/google/search"
    assert seen["api_key"] == "test-key"
    assert seen["source"] == "pytest"
    assert '"q":"python"' in seen["payload"]


@pytest.mark.asyncio
async def test_request_raises_for_api_error():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"status": 1020, "error": "insufficient credits"})

    client = SerpBaseClient(
        Settings(api_key="test-key", base_url="https://api.example.test"),
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(SerpBaseError) as excinfo:
        await client.request("search", {"q": "python"})

    assert "insufficient credits" in str(excinfo.value)
    assert excinfo.value.api_status == 1020


def test_query_payload_validates_maps_coordinates():
    with pytest.raises(ValueError, match="lat and lng"):
        query_payload("coffee", lat=37.7)

    payload = query_payload("coffee", lat=37.7, lng=-122.4)
    assert payload["zoom"] == 14


def test_maps_detail_payload_requires_feature_id():
    with pytest.raises(ValueError, match="feature_id"):
        maps_detail_payload("")
