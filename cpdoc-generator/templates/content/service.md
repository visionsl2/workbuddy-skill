{# 服务与支持模板 - Service and Support Template #}

# 7. 服务与支持

## 7.1 质保服务

{% if warranty %}
- **质保期限：** {{ warranty.period | default("12个月") }}
- **质保范围：** {{ warranty.scope | default("整机质保") }}
- **响应时效：** {{ warranty.response_time | default("7×24小时响应") }}
{% else %}
- **质保期限：** 12个月
- **质保范围：** 硬件设备质保12个月，软件平台运维12个月
- **响应时效：** 7×24小时响应，普通故障4小时到场
{% endif %}

## 7.2 运维服务

{% if maintenance %}
- **质保期后：** {{ maintenance.after_warranty | default("可选年度维保服务") }}
- **服务内容：**
{% for item in maintenance.内容包括 | default([]) %}
  - {{ item }}
{% endfor %}
{% else %}
- **质保期后：** 可选年度维保服务
- **服务内容：**
  - 系统巡检与优化
  - 安全补丁更新
  - 故障响应处理
{% endif %}

## 7.3 培训计划

{% if training %}
- **培训安排：** {{ training.training_plan | default("提供现场培训") }}
- **培训资料：**
{% for material in training.training_materials | default([]) %}
  - {{ material }}
{% endfor %}
- **培训学时：** {{ training.training_hours | default("不少于16学时") }}
{% else %}
- **培训安排：** 提供现场培训
- **培训资料：** 用户手册、培训视频
- **培训学时：** 不少于16学时
{% endif %}

## 7.4 交付文档

{% if documentation.deliverables %}
{% for doc in documentation.deliverables %}
- {{ doc }}
{% endfor %}
{% else %}
- 项目实施方案
- 系统操作手册
- 运维管理手册
- 竣工验收报告
{% endif %}
