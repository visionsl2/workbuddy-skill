# WorkBuddy Skills

存放 WorkBuddy 的自定义技能（Skill）。

## 目录结构

```
workbuddy-skills/
├── dify-knowledge-bridge/     # Dify 企业知识库桥接器
│   ├── SKILL.md               # 技能说明
│   ├── scripts/               # MCP Server 脚本
│   └── references/            # 参考文档
└── README.md
```

## dify-knowledge-bridge

连接公司 Dify 知识库的 MCP Server，支持语义搜索。

**使用前配置：**
1. 确保 `scripts/dify_mcp_config.json` 中的 endpoint、api_key、knowledge_id 正确
2. 在 WorkBuddy 中启用此技能

**MCP 配置：**
```json
{
  "mcpServers": {
    "dify-knowledge-bridge": {
      "command": "python",
      "args": ["/path/to/skills/dify-knowledge-bridge/scripts/dify_mcp_server.py"]
    }
  }
}
```
