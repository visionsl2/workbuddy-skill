# Dify 知识库桥接器 - 部署指南

## 概述

本 Skill 实现 WorkBuddy 与公司 Dify 知识库的桥接，让所有同事可以通过自然语言搜索公司知识库。

## 部署步骤

### 1. 复制文件到同事电脑

将整个 `dify-knowledge-bridge` 文件夹复制到：
```
C:\Users\<用户名>\.workbuddy\skills\dify-knowledge-bridge
```

### 2. 配置连接信息

编辑 `scripts/dify_mcp_config.json`：

```json
{
    "dify_endpoint": "http://160.0.6.9/v1",
    "dify_api_key": "dataset-GeVY5VrH2Uu0cgr931oLHaze",
    "knowledge_id": "你的知识库ID",
    "top_k": 3,
    "score_threshold": 0.5
}
```

### 3. 在 WorkBuddy 中启用 MCP

1. 打开 WorkBuddy
2. 进入「插件」→「MCP 服务器」
3. 点击「配置 MCP」
4. 编辑 `mcp.json`，添加：

```json
{
  "mcpServers": {
    "dify-knowledge": {
      "command": "python",
      "args": ["C:\\Users\\用户名\\.workbuddy\\skills\\dify-knowledge-bridge\\scripts\\dify_mcp_server.py"]
    }
  }
}
```

### 4. 重启 WorkBuddy

MCP Server 状态变为绿色即成功。

### 5. 获取知识库 ID

在 Dify 后台 → 知识库 → 点击具体知识库 → URL 中可看到 ID

## IT 管理员批量部署

可以写一个 PowerShell 脚本批量部署到所有电脑。
