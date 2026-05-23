from __future__ import annotations

import json

import pytest


@pytest.mark.asyncio
async def test_list_tools_exposes_serpbase_tools():
    from serpbase_mcp import broker

    tools = await broker.list_tools()
    names = {tool.name for tool in tools}

    assert {
        "serpbase_search",
        "serpbase_images",
        "serpbase_news",
        "serpbase_videos",
        "serpbase_maps_search",
        "serpbase_maps_detail",
    } <= names


@pytest.mark.asyncio
async def test_call_tool_serializes_errors():
    from serpbase_mcp import broker

    response = await broker.call_tool("serpbase_search", {"query": ""})
    payload = json.loads(response[0].text)

    assert payload["tool"] == "serpbase_search"
    assert "query is required" in payload["error"]
