# WorkBuddy Skills

存放 WorkBuddy 的自定义技能（Skill）。所有技能统一管理，统一发布到 `main` 分支。

## 版本记录

| 技能 | 版本 | 更新日期 | 更新内容 |
|------|------|----------|----------|
| cpdoc-generator | V2.1 | 2026-04-15 | 完善双层章节结构与图片命名规范 |
| dify-knowledge-bridge | V1.0 | 2026-04 | 首次发布，支持 Dify 知识库桥接 |

## 目录结构

```
workbuddy-skill/
├── cpdoc-generator/             # 物联网解决方案文档生成器 V2.1
│   ├── SKILL.md               # 技能说明
│   ├── src/                   # 生成器源码
│   ├── templates/             # 文档模板
│   └── data/                  # 项目数据
├── dify-knowledge-bridge/      # Dify 企业知识库桥接器 V1.0
│   ├── SKILL.md               # 技能说明
│   ├── scripts/               # MCP Server 脚本
│   └── references/            # 参考文档
└── README.md
```

---

## cpdoc-generator (V2.1)

物联网(IoT)解决方案文档生成器，用于从会议纪要或需求文档自动生成专业的 Word 解决方案文档。

**核心能力：**
- Word 文档解析 - 读取参考方案，提取结构、内容、图片
- 会议纪要解析 - 从 .md/.docx 纪要中提取客户、设备、需求
- 自动生成符合模板的数据文件
- 基于 Jinja2 模板和数据生成最终 Word 文档

**章节结构规范：**

| 章节 | 内容 | 来源 |
|------|------|------|
| 1. 项目概述 | 项目背景、建设目标 | 会议纪要 |
| 2. 需求分析 | 痛点分析、业务目标 | 会议纪要 |
| 3. 解决方案设计 | 系统架构、技术方案 | 复用参考方案 |
| 4. 产品选型清单 | 硬件/软件清单 | 会议纪要 |
| 5. 软件平台介绍 | 平台功能模块 | **复用参考方案（第5章）** |
| 6. 实施计划 | 实施阶段计划 | 会议纪要 |
| 7. 服务与支持 | 售后服务 | 模板 |
| 8. 附录 | 报价、技术指标 | 会议纪要 |

**图片命名规范：**
- 参考方案图片：`image11.png`, `image12.png`, ...
- 模块图片字段：`image`, `image1`, `image2`, ...

---

## dify-knowledge-bridge (V1.0)

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

---

## 添加新技能

新技能请添加到对应目录，并更新本文件的版本记录。

**命名规范：**
- 技能目录名：`kebab-case`（如 `my-new-skill`）
- SKILL.md 必须包含 `name`、`version`、`description` 字段
