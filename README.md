# SerpBase MCP

[中文文档](README.zh-CN.md)

Connect the [SerpBase](https://serpbase.dev) Google Search, Images, News, Videos, and Maps APIs to any AI agent that supports MCP.

Use this server when you want to:

- Give Claude, Codex, Cursor, Cline/Roo, Continue, or another MCP client real-time Google search.
- Ground RAG, market research, SEO, competitor monitoring, or brand monitoring workflows with structured SERP data.
- Query Google Images, News, Videos, Maps local search, and Maps place details as JSON.

## Features

| MCP tool | SerpBase API | Use case |
| --- | --- | --- |
| `serpbase_search` | `/google/search` | Google Search results, organic links, related searches, knowledge graph, and other SERP modules |
| `serpbase_images` | `/google/images` | Image URLs, thumbnails, source pages, and domains |
| `serpbase_news` | `/google/news` | News titles, publishers, time text, snippets, and thumbnails |
| `serpbase_videos` | `/google/videos` | Video links, sources, durations, time text, and thumbnails |
| `serpbase_maps_search` | `/google/maps/search` | Google Maps local place search |
| `serpbase_maps_detail` | `/google/maps/detail` | Place detail lookup by `feature_id` |

## Get an API key

1. Open [SerpBase API Keys](https://serpbase.dev/dashboard/api-keys).
2. Create or copy an API key.
3. Pass it to your MCP client as an environment variable:

```bash
SERPBASE_API_KEY=your_serpbase_api_key
```

Do not commit API keys to public repositories.

## Installation

Install from GitHub:

```bash
git clone https://github.com/serpbase-dev/serpbase-mcp.git
cd serpbase-mcp
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e .
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e .
```

You can also run it as a Python module:

```bash
python -m pip install -e .
python -m serpbase_mcp
```

## MCP configuration

### Generic config

If the `serpbase-mcp` command is available on PATH:

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

If the command is not on PATH, run the module directly:

```json
{
  "mcpServers": {
    "serpbase": {
      "command": "python",
      "args": ["-m", "serpbase_mcp"],
      "cwd": "/absolute/path/to/serpbase-mcp",
      "env": {
        "SERPBASE_API_KEY": "your_serpbase_api_key"
      }
    }
  }
}
```

Windows path example:

```json
{
  "mcpServers": {
    "serpbase": {
      "command": "python",
      "args": ["-m", "serpbase_mcp"],
      "cwd": "C:\\Users\\you\\work\\serpbase-mcp",
      "env": {
        "SERPBASE_API_KEY": "your_serpbase_api_key"
      }
    }
  }
}
```

### Claude Desktop

Add the `mcpServers` block above to your Claude Desktop config:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop. The `serpbase_*` tools should appear in the tool list.

### Cursor / Cline / Roo / Continue

The UI differs by client, but the config is the same: add a stdio MCP server named `serpbase`, set `command` to `serpbase-mcp` or `python -m serpbase_mcp`, and pass `SERPBASE_API_KEY` in `env`.

## Usage examples

### Google Search

Call `serpbase_search`:

```json
{
  "query": "python asyncio tutorial",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

Prompt example:

```text
Use SerpBase to search for recent articles about Python asyncio and summarize the top results with links.
```

### Google Images

Call `serpbase_images`:

```json
{
  "query": "iphone 15 pro blue",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

Important fields: `images[].image_url`, `thumbnail_url`, `link`, and `domain`.

### Google News

Call `serpbase_news`:

```json
{
  "query": "apple event",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

Important fields: `news[].title`, `source`, `time`, `published_at`, `snippet`, and `link`.

### Google Videos

Call `serpbase_videos`:

```json
{
  "query": "python asyncio tutorial",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

Important fields: `videos[].title`, `source`, `duration`, `time`, and `link`.

### Google Maps local search

Call `serpbase_maps_search`:

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

`lat` and `lng` must be sent together. Important fields: `places[].name`, `feature_id`, `rating`, `address`, `phone`, `website`, `google_maps_url`, `latitude`, and `longitude`.

### Google Maps place detail

Get a `feature_id` from `serpbase_maps_search`, then call `serpbase_maps_detail`:

```json
{
  "feature_id": "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123",
  "hl": "en",
  "gl": "us"
}
```

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SERPBASE_API_KEY` | Yes | None | SerpBase API key |
| `SERPBASE_BASE_URL` | No | `https://api.serpbase.dev` | Override only for testing or private gateways |
| `SERPBASE_TIMEOUT` | No | `30` | Request timeout in seconds |
| `SERPBASE_SOURCE` | No | `serpbase-mcp` | Value sent as `X-SerpBase-Source` |

## Local tests

```bash
pip install -e ".[dev]"
python -m pytest
```

Quick import check:

```bash
python -c "from serpbase_mcp.broker import _TOOLS; print([t.name for t in _TOOLS])"
```

## Troubleshooting

### The client cannot find `serpbase-mcp`

Use module mode:

```json
{
  "command": "python",
  "args": ["-m", "serpbase_mcp"],
  "cwd": "/absolute/path/to/serpbase-mcp"
}
```

### `SERPBASE_API_KEY is not set`

Add the key to your MCP server environment:

```json
{
  "SERPBASE_API_KEY": "your_serpbase_api_key"
}
```

Restart the MCP client after changing the config.

### `status: 1020`

The account does not have enough credits. Add credits in the SerpBase dashboard or use another valid API key.

### The agent answers without source links

Ask the agent to cite the `link`, `url`, `display_url`, or `google_maps_url` fields returned by SerpBase.

## License

MIT
