{# 项目概述模板 - Executive Summary Template #}

# 1. 项目概述

## 1.1 方案概述

{{ overview }}

## 1.2 核心价值

{% if key_benefits %}
{{ key_benefits }}
{% else %}
- 提升运营效率
- 降低运营成本
- 增强数据可视化能力
{% endif %}
