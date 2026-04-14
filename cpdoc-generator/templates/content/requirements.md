{# 需求分析模板 - Requirements Analysis Template #}

# 2. 需求分析

## 2.1 项目背景

{{ background }}

## 2.2 业务痛点

{% if pain_points %}
{% for pain in pain_points %}
### 2.2.{{ loop.index }} {{ pain.title }}

{{ pain.description }}

{% endfor %}
{% else %}
暂无痛点数据。
{% endif %}

## 2.3 建设目标

{% if business_goals %}
{% for goal in business_goals %}
- {{ goal }}
{% endfor %}
{% else %}
- 实现数字化转型
- 提升运营效率
{% endif %}
