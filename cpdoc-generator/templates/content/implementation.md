{# 实施计划模板 - Implementation Plan Template #}

# 6. 实施计划

## 6.1 项目周期

{{ overview | default("项目总工期需根据实际方案确定。") }}

## 6.2 实施阶段

{% if phases %}
| 阶段 | 名称 | 工期 | 主要交付物 | 里程碑 |
|:-----|:-----|:----:|:-----------|:-------|
{% for phase in phases %}
| 第{{ phase.phase_no }}阶段 | {{ phase.phase_name }} | {{ phase.duration }} | {% for d in phase.deliverables %}{{ d }}{% if not loop.last %}、{% endif %}{% endfor %} | {{ phase.milestone }} |
{% endfor %}
{% else %}
暂无实施阶段数据。
{% endif %}

## 6.3 质量保障

{% if quality_control %}
{% for qc in quality_control %}
- {{ qc }}
{% endfor %}
{% else %}
- 每阶段设置评审检查点
- 关键节点验收测试
{% endif %}

## 6.4 风险识别与应对

{% if risks_and_mitigation %}
| 风险项 | 应对措施 |
|:-------|:---------|
{% for risk in risks_and_mitigation %}
| {{ risk.risk }} | {{ risk.mitigation }} |
{% endfor %}
{% else %}
| 风险项 | 应对措施 |
|:-------|:---------|
| 待补充 | 待补充 |
{% endif %}
