---
name: dify-knowledge-bridge
version: "1.0"
description: >
  This skill should be used when the user needs to search the company's shared
  Dify knowledge base from WorkBuddy, or when configuring WorkBuddy MCP to
  connect with Dify for enterprise knowledge retrieval. It provides a complete
  MCP server bridge that queries Dify's external knowledge API and returns
  structured results.
---

# Dify 知识库桥接器

WorkBuddy 与公司 Dify 知识库的桥接方案，实现语义搜索功能。

## 工作原理

```
WorkBuddy  ──MCP──▶  dify_mcp_server.py  ──HTTP──▶  Dify 知识库 API
```

## 使用场景

当用户询问公司知识库相关内容时使用，例如：
- "查一下公司的年假政策"
- "告诉我们入职培训流程"
- "公司报销流程是什么"
- 任何需要从公司文档中查找答案的问题

## MCP 工具

### search_dify_knowledge

**功能：** 搜索公司 Dify 知识库

**参数：**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | 是 | - | 搜索关键词或问题 |
| top_k | integer | 否 | 3 | 返回结果数量 |

**返回值：** 格式化的问题答案，包含来源文档信息

## 配置信息

已配置连接到公司 Dify 服务器：
- **Endpoint:** http://160.0.6.9/v1
- **API Key:** dataset-GeVY5VrH2Uu0cgr931oLHaze

## 文件结构

```
dify-knowledge-bridge/
├── SKILL.md                           # 本文件
├── scripts/
│   ├── dify_mcp_server.py            # MCP Server 主程序
│   ├── dify_mcp_config.json          # 配置文件
│   └── test_dify_connection.py        # 连接测试脚本
└── references/
    └── deployment-guide.md            # 详细部署指南
```

## 故障排除

### MCP Server 显示红色
1. 检查 Python 依赖：`pip install mcp requests`
2. 检查配置文件 JSON 格式
3. 查看 WorkBuddy 日志

### 搜索无结果
1. 确认 Dify 知识库中已有文档
2. 测试 Dify API：`curl http://160.0.6.9/health`
