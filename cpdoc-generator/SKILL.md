---
name: cpdoc-generator
description: |
  物联网(IoT)解决方案文档生成器。用于从会议纪要或需求文档自动生成专业的Word解决方案文档。
  当用户需要生成物联网解决方案、设备数采方案、智能制造方案等Word文档时触发此skill。
  支持从参考方案中提取模板结构、内容和图片，自动填充客户定制化信息。
---

# CPDoc Generator - 物联网解决方案文档生成器

## 概述

本skill用于自动生成物联网解决方案Word文档。核心工作流程：

```
会议纪要/需求文档 → YAML数据文件 → Word解决方案文档
```

## 核心能力

1. **Word文档解析** - 读取参考方案(.docx)，提取结构、内容、图片
2. **会议纪要解析** - 从.md/.docx纪要中提取客户、设备、需求等信息
3. **YAML数据生成** - 自动生成符合模板的数据文件
4. **文档生成** - 基于Jinja2模板和数据生成最终Word文档

## 使用流程

### Step 1: 收集输入材料

用户提供以下材料（至少提供一项）：
- **参考方案**（.docx格式）- 可从公司历史项目中获取
- **会议纪要**（.md/.docx格式）- 记录客户需求
- **客户基本信息** - 公司名、行业、设备类型等

### Step 2: 提取参考方案（可选）

若提供了参考方案，执行以下命令提取内容和图片：

```bash
python src/word2yaml.py --input <参考方案路径> --output <输出YAML路径>
```

### Step 3: 生成或更新YAML数据

基于会议纪要和参考方案，生成客户专属的YAML数据文件。

关键字段说明：

| 字段 | 说明 | 示例 |
|------|------|------|
| `project_name` | 项目名称 | "心宝药业IoT数据采集项目" |
| `customer` | 客户名称 | "心宝药业" |
| `industry` | 行业 | "制药" |
| `date` | 文档日期 | "2026-04" |
| `device_count` | 设备数量 | 30 |
| `device_types` | 设备类型列表 | ["压片机", "包衣机", "带式干燥机"] |
| `pain_points` | 痛点列表 | [{title, description}] |
| `platform_modules` | 平台模块（含图片） | [{title, description, image, image1, image2}] |

### Step 4: 生成文档

```bash
python src/generator.py --project <YAML路径> --template <模板名> --output <输出目录>
```

## 项目结构

本skill依赖 iot_doc_generator 项目，位于工作区：

```
iot_doc_generator/
├── src/
│   ├── generator.py      # 主生成器
│   ├── data_loader.py    # 数据加载器
│   ├── template_engine.py # 模板引擎
│   ├── doc_builder.py    # Word文档构建器
│   └── word2yaml.py      # Word转YAML工具
├── templates/standard/   # 标准解决方案模板
│   ├── content/          # 各章节Markdown模板
│   └── assets/          # 模板资源
├── data/projects/       # 项目数据
│   └── xxx.yaml         # 各客户YAML数据
└── assets/images/ygdn/  # 参考方案图片
```

## 章节结构

标准物联网解决方案包含以下章节：

| 章节 | 内容 | 来源 |
|------|------|------|
| 1. 项目概述 | 项目背景、建设目标 | 会议纪要 |
| 1.1 项目背景 | 行业背景、客户现状 | 会议纪要 |
| 1.2 核心价值 | 5个核心价值点 | 会议纪要+模板 |
| 2. 需求分析 | 痛点分析、业务目标 | 会议纪要 |
| 3. 解决方案设计 | 系统架构、技术方案 | 复用参考方案 |
| 4. 产品选型清单 | 硬件/软件清单 | 会议纪要 |
| 5. 软件平台介绍 | 平台功能模块 | **复用参考方案（第5章）** |
| 6. 实施计划 | 实施阶段计划 | 会议纪要 |
| 7. 服务与支持 | 售后服务 | 模板 |
| 8. 附录 | 报价、技术指标 | 会议纪要 |

## 图片处理

### 从参考方案提取图片

```python
from docx import Document
doc = Document('参考方案.docx')
for rel_id, rel in doc.part.rels.items():
    if 'image' in rel.target_ref:
        img_part = rel.target_part
        # 保存图片
```

### 图片命名规范

参考方案图片按序号命名：`image11.png`, `image12.png`, ...

模块图片字段：`image`, `image1`, `image2`, `image3`, ...

### 第5章图片分配（标准模板）

| 模块 | 图片数量 | 图片编号 |
|------|:--------:|----------|
| 5.1 设备管理 | 4张 | image11-14 |
| 5.2 数据管理 | 0张 | - |
| 5.3 采集对象配置 | 3张 | image15-17 |
| 5.4 网关管理 | 1张 | image18 |
| 5.5 协议管理 | 2张 | image19-20 |
| 5.6 接口与服务 | 1张 | image21 |
| 5.7 指令下发 | 0张 | - |
| 5.8 平台管理 | 3张 | image22-24 |

## 模板字段命名

| 用途 | 字段名 | 说明 |
|------|--------|------|
| 主图 | `image` | 模块主图 |
| 额外图 | `image1`, `image2`, `image3`... | 最多支持6张 |

**注意**：不要使用 `image2`, `image3` 作为额外图，应使用 `image1`, `image2`...

## 字体规范

| 元素 | 字体 | 大小 |
|------|------|------|
| 正文 | 宋体 | 10.5pt |
| 标题1 | 黑体 | 14pt |
| 标题2 | 黑体 | 12pt |
| 封面标题 | 黑体 | 26pt |

## 输出文档

生成的文件命名规范：
```
<客户名>_<项目名>_<版本号>.docx
示例：心宝药业IoT数据采集与智能平台项目_V15.docx
```

## 注意事项

1. **章节标题样式** - 大章节使用"标题1"（Word内置样式），小章节使用"标题2"
2. **第5章固定** - 5.软件平台介绍章节内容固定，不做更改
3. **图片路径** - 使用相对路径：`assets/images/ygdn/imageXX.png`
4. **YAML格式** - 确保图片字段使用 `image`, `image1`, `image2` 而非 `image2`, `image3`

## 快速开始

1. 用户提供会议纪要
2. 提取/创建YAML数据文件
3. 运行 `python src/generator.py --project <yaml> --template standard --output output/`
4. 打开生成的.docx文件供用户审核
