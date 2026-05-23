# SerpBase MCP

[English](README.md)

面向 AI Agent、搜索 grounding、RAG、SEO 工具和本地商家数据工作流的 Google SERP API MCP Server。

把 [SerpBase](https://serpbase.dev) 的 Google Search、Images、News、Videos 和 Maps API 接入任何支持 MCP 的 AI Agent。

适合这些场景：

- 给 Claude、Codex、Cursor、Cline/Roo、Continue 等 Agent 增加实时 Google 搜索能力
- 给 RAG、市场调研、SEO、竞品监控、品牌监控做搜索 grounding
- 查询 Google Images / News / Videos / Maps 并拿到结构化 JSON

## 功能

| MCP 工具 | 对应 SerpBase API | 用途 |
| --- | --- | --- |
| `serpbase_search` | `/google/search` | Google Search 结果、自然链接、相关搜索、知识图谱等 SERP 模块 |
| `serpbase_images` | `/google/images` | 图片 URL、缩略图、来源页面、域名 |
| `serpbase_news` | `/google/news` | 新闻标题、来源、时间、摘要、缩略图 |
| `serpbase_videos` | `/google/videos` | 视频链接、来源、时长、发布时间、缩略图 |
| `serpbase_maps_search` | `/google/maps/search` | Google Maps 本地地点搜索 |
| `serpbase_maps_detail` | `/google/maps/detail` | 通过 `feature_id` 获取单个地点详情 |

## 准备 API Key

1. 打开 [SerpBase API Keys](https://serpbase.dev/dashboard/api-keys)
2. 创建或复制一个 API key
3. 配到 MCP 客户端环境变量里：

```bash
SERPBASE_API_KEY=your_serpbase_api_key
```

不要把 API key 写进公开仓库。

## 安装

当前推荐从 GitHub 安装：

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

如果你只想直接跑，也可以不用激活虚拟环境：

```bash
python -m pip install -e .
python -m serpbase_mcp
```

## MCP 客户端配置

### 通用配置

如果 `serpbase-mcp` 命令在 PATH 里：

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

如果命令不在 PATH，使用模块启动更稳：

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

Windows 路径示例：

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

把上面的 `mcpServers` 加到 Claude Desktop 配置文件：

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

重启 Claude Desktop 后，工具列表里应能看到 `serpbase_*` 工具。

### Cursor / Cline / Roo / Continue

这些工具的 MCP 配置入口略有不同，但内容相同：添加一个名为 `serpbase` 的 stdio MCP server，`command` 指向 `serpbase-mcp` 或 `python -m serpbase_mcp`，并传入 `SERPBASE_API_KEY`。

## 调用示例

### 1. 普通 Google 搜索

让 Agent 调用 `serpbase_search`：

```json
{
  "query": "python asyncio tutorial",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

适合提示词：

```text
Use SerpBase to search for recent articles about Python asyncio and summarize the top results with links.
```

### 2. 图片搜索

调用 `serpbase_images`：

```json
{
  "query": "iphone 15 pro blue",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

返回里重点看 `images[].image_url`、`thumbnail_url`、`link`、`domain`。

### 3. 新闻搜索

调用 `serpbase_news`：

```json
{
  "query": "apple event",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

返回里重点看 `news[].title`、`source`、`time`、`published_at`、`snippet`、`link`。

### 4. 视频搜索

调用 `serpbase_videos`：

```json
{
  "query": "python asyncio tutorial",
  "hl": "en",
  "gl": "us",
  "page": 1
}
```

返回里重点看 `videos[].title`、`source`、`duration`、`time`、`link`。

### 5. Google Maps 本地搜索

调用 `serpbase_maps_search`：

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

`lat` 和 `lng` 必须一起传。返回里重点看 `places[].name`、`feature_id`、`rating`、`address`、`phone`、`website`、`google_maps_url`、`latitude`、`longitude`。

### 6. Google Maps 地点详情

先从 `serpbase_maps_search` 结果中拿到 `feature_id`，再调用 `serpbase_maps_detail`：

```json
{
  "feature_id": "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123",
  "hl": "en",
  "gl": "us"
}
```

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SERPBASE_API_KEY` | 是 | 无 | SerpBase API key |
| `SERPBASE_BASE_URL` | 否 | `https://api.serpbase.dev` | 仅在测试或私有网关时需要改 |
| `SERPBASE_TIMEOUT` | 否 | `30` | 请求超时秒数 |
| `SERPBASE_SOURCE` | 否 | `serpbase-mcp` | 发送到 `X-SerpBase-Source` 的来源标记 |

## 本地测试

```bash
pip install -e ".[dev]"
python -m pytest
```

也可以快速检查工具是否能导入：

```bash
python -c "from serpbase_mcp.broker import _TOOLS; print([t.name for t in _TOOLS])"
```

## 常见问题

### 1. 客户端提示找不到 `serpbase-mcp`

说明 console script 不在 PATH。改用：

```json
{
  "command": "python",
  "args": ["-m", "serpbase_mcp"],
  "cwd": "/absolute/path/to/serpbase-mcp"
}
```

### 2. 返回 `SERPBASE_API_KEY is not set`

在 MCP 配置的 `env` 里添加：

```json
{
  "SERPBASE_API_KEY": "your_serpbase_api_key"
}
```

配置后重启 MCP 客户端。

### 3. 返回 `status: 1020`

账号 credits 不足。去 SerpBase 控制台充值或换一个有余额的 API key。

### 4. Agent 没有引用链接

提示 Agent 使用结果里的 `link`、`url`、`display_url`、`google_maps_url` 字段作为引用来源，并要求“答案中附上来源链接”。

## License

MIT
