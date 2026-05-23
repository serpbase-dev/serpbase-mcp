"""MCP server exposing SerpBase tools over stdio."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions

from serpbase_mcp import __version__
from serpbase_mcp.client import SerpBaseClient, maps_detail_payload, query_payload

server = Server("serpbase-mcp")


QUERY_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "description": "Search query"},
        "hl": {"type": "string", "default": "en", "description": "Google language code"},
        "gl": {"type": "string", "default": "us", "description": "Google country code"},
        "page": {"type": "integer", "default": 1, "minimum": 1},
    },
    "required": ["query"],
}

MAPS_SEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        **QUERY_SCHEMA["properties"],
        "lat": {"type": "number", "minimum": -90, "maximum": 90},
        "lng": {"type": "number", "minimum": -180, "maximum": 180},
        "zoom": {"type": "integer", "default": 14, "minimum": 1, "maximum": 21},
    },
    "required": ["query"],
}

MAPS_DETAIL_SCHEMA = {
    "type": "object",
    "properties": {
        "feature_id": {
            "type": "string",
            "description": "Google Maps feature_id returned by serpbase_maps_search",
        },
        "hl": {"type": "string", "default": "en"},
        "gl": {"type": "string", "default": "us"},
    },
    "required": ["feature_id"],
}

_TOOLS = [
    types.Tool(
        name="serpbase_search",
        description="Search Google through SerpBase and return organic results plus rich SERP modules.",
        inputSchema=QUERY_SCHEMA,
    ),
    types.Tool(
        name="serpbase_images",
        description="Search Google Images through SerpBase and return image URLs, thumbnails, source pages, and domains.",
        inputSchema=QUERY_SCHEMA,
    ),
    types.Tool(
        name="serpbase_news",
        description="Search Google News through SerpBase and return articles with publisher, time, snippet, and thumbnails when available.",
        inputSchema=QUERY_SCHEMA,
    ),
    types.Tool(
        name="serpbase_videos",
        description="Search Google Videos through SerpBase and return video links with source, duration, time, and thumbnails.",
        inputSchema=QUERY_SCHEMA,
    ),
    types.Tool(
        name="serpbase_maps_search",
        description="Search Google Maps through SerpBase and return local place results. Optional lat/lng/zoom can geo-target the query.",
        inputSchema=MAPS_SEARCH_SCHEMA,
    ),
    types.Tool(
        name="serpbase_maps_detail",
        description="Fetch Google Maps place details through SerpBase for a feature_id returned by serpbase_maps_search.",
        inputSchema=MAPS_DETAIL_SCHEMA,
    ),
]

_TOOL_TYPES = {
    "serpbase_search": "search",
    "serpbase_images": "images",
    "serpbase_news": "news",
    "serpbase_videos": "videos",
    "serpbase_maps_search": "maps_search",
}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return _TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    try:
        result = await dispatch_tool(name, arguments or {})
    except Exception as exc:
        result = {"error": str(exc), "tool": name}
    return [
        types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False),
        )
    ]


async def dispatch_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    client = SerpBaseClient()
    if name in _TOOL_TYPES:
        payload = query_payload(
            arguments.get("query", ""),
            hl=arguments.get("hl", "en"),
            gl=arguments.get("gl", "us"),
            page=int(arguments.get("page", 1)),
            lat=arguments.get("lat"),
            lng=arguments.get("lng"),
            zoom=arguments.get("zoom"),
        )
        return await client.request(_TOOL_TYPES[name], payload)

    if name == "serpbase_maps_detail":
        payload = maps_detail_payload(
            arguments.get("feature_id", ""),
            hl=arguments.get("hl", "en"),
            gl=arguments.get("gl", "us"),
        )
        return await client.request("maps_detail", payload)

    return {"error": f"Unknown tool: {name}"}


async def _main() -> None:
    options = InitializationOptions(
        server_name="serpbase-mcp",
        server_version=__version__,
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        ),
    )
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)


def run() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    run()
