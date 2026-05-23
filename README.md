# SerpBase MCP

MCP server for calling the SerpBase Google SERP APIs from Claude, Codex, Cursor, Cline/Roo, Continue, and other MCP clients.

It exposes six tools:

- `serpbase_search`: Google Search results and rich SERP modules.
- `serpbase_images`: Google Images results.
- `serpbase_news`: Google News results.
- `serpbase_videos`: Google Videos results.
- `serpbase_maps_search`: Google Maps local place results.
- `serpbase_maps_detail`: Google Maps place detail by `feature_id`.

## Install

```bash
cd opensource/serpbase-mcp
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -e .
```

Set your API key:

```bash
set SERPBASE_API_KEY=your_serpbase_api_key
```

PowerShell:

```powershell
$env:SERPBASE_API_KEY = "your_serpbase_api_key"
```

## MCP config

```json
{
  "mcpServers": {
    "serpbase": {
      "command": "serpbase-mcp",
      "env": {
        "SERPBASE_API_KEY": "your_serpbase_api_key"
      }
    }
  }
}
```

For local development without installing the console script:

```json
{
  "mcpServers": {
    "serpbase": {
      "command": "python",
      "args": ["-m", "serpbase_mcp"],
      "cwd": "/absolute/path/to/opensource/serpbase-mcp",
      "env": {
        "SERPBASE_API_KEY": "your_serpbase_api_key"
      }
    }
  }
}
```

## Examples

Search:

```json
{
  "query": "python asyncio",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

Maps search:

```json
{
  "query": "coffee",
  "hl": "en",
  "gl": "us",
  "page": 1,
  "lat": 37.7749,
  "lng": -122.4194,
  "zoom": 14
}
```

Maps detail:

```json
{
  "feature_id": "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123",
  "hl": "en",
  "gl": "us"
}
```

## Environment

- `SERPBASE_API_KEY` is required.
- `SERPBASE_BASE_URL` defaults to `https://api.serpbase.dev`.
- `SERPBASE_TIMEOUT` defaults to `30` seconds.
- `SERPBASE_SOURCE` defaults to `serpbase-mcp` and is sent as `X-SerpBase-Source`.

## Test

```bash
pip install -e ".[dev]"
pytest
```
