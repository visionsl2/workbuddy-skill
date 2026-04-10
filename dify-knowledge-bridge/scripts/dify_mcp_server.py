#!/usr/bin/env python3
"""
Dify 知识库 MCP Server
桥接 WorkBuddy 与 Dify 知识库，实现语义搜索功能
"""

import json
import logging
import os
from mcp.server.fastmcp import FastMCP
import requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dify-knowledge-mcp")

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 加载配置
CONFIG_PATH = os.path.join(SCRIPT_DIR, "dify_mcp_config.json")

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error("配置文件 dify_mcp_config.json 未找到")
    config = {}

DIFY_ENDPOINT = config.get("dify_endpoint", "")
DIFY_API_KEY = config.get("dify_api_key", "")
KNOWLEDGE_ID = config.get("knowledge_id", "")
DEFAULT_TOP_K = config.get("top_k", 3)
DEFAULT_SCORE_THRESHOLD = config.get("score_threshold", 0.5)

# 初始化 MCP Server
mcp = FastMCP("Dify知识库助手")


def search_dify_api(query: str, top_k: int = DEFAULT_TOP_K,
                    score_threshold: float = DEFAULT_SCORE_THRESHOLD) -> dict:
    """调用 Dify 知识库检索 API"""
    # Dify 知识库检索接口格式
    url = f"{DIFY_ENDPOINT}/datasets/{KNOWLEDGE_ID}/retrieve"

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "retrieval_setting": {
            "top_k": top_k,
            "score_threshold": score_threshold
        }
    }

    logger.info(f"搜索请求: query={query}, top_k={top_k}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API 请求失败: {e}")
        return {"error": str(e), "records": []}


def format_search_results(result: dict) -> str:
    """格式化搜索结果"""
    if "error" in result:
        return f"搜索失败：{result['error']}"

    records = result.get("records", [])

    if not records:
        return "未找到相关知识内容，请尝试其他关键词。"

    output_parts = []
    output_parts.append(f"找到 {len(records)} 条相关知识：\n")

    for i, record in enumerate(records, 1):
        # 优先从 segment.document.name 获取文档名，其次用 segment.title，最后用 content 前50字
        segment = record.get("segment", {})
        document = segment.get("document", {})
        content = segment.get("content", "")

        # 文档名：优先用 document.name，否则用 segment 的 title 或 content 前50字
        title = document.get("name") or segment.get("title") or (content[:50] + "..." if len(content) > 50 else content)

        score = record.get("score", 0)

        match_emoji = "🟢" if score >= 0.8 else "🟡" if score >= 0.6 else "🔵"

        output_parts.append(f"{match_emoji} [{i}] {title}")
        output_parts.append(f"   {content}")

        if document.get("name"):
            output_parts.append(f"   来源: {document['name']}")

        output_parts.append("")

    return "\n".join(output_parts)


@mcp.tool()
def search_dify_knowledge(query: str, top_k: int = 3) -> str:
    """
    搜索公司 Dify 知识库

    Args:
        query: 搜索关键词或问题（必填）
        top_k: 返回结果数量，默认为 3条

    Returns:
        格式化的问题答案，包含来源文档信息
    """
    if not query or not query.strip():
        return "请提供搜索关键词或问题"

    query = query.strip()
    logger.info(f"执行知识库搜索: {query}")

    result = search_dify_api(query, top_k=top_k, score_threshold=0.5)
    return format_search_results(result)


@mcp.tool()
def check_dify_connection() -> str:
    """检查 Dify 知识库连接状态"""
    if not DIFY_ENDPOINT:
        return "未配置 Dify 服务器地址"
    if not DIFY_API_KEY:
        return "未配置 Dify API Key"
    if not KNOWLEDGE_ID or KNOWLEDGE_ID == "你的知识库ID":
        return "未配置知识库 ID"

    try:
        result = search_dify_api("连接测试", top_k=1)
        if "error" in result:
            return f"连接失败：{result['error']}"
        return "Dify 知识库连接正常！"
    except Exception as e:
        return f"连接异常：{str(e)}"


if __name__ == "__main__":
    logger.info("启动 Dify 知识库 MCP Server...")
    logger.info(f"Endpoint: {DIFY_ENDPOINT}")
    mcp.run()
