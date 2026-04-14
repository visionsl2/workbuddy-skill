{# 解决方案设计模板 - Solution Design Template #}

# 3. 解决方案设计

## 3.1 架构设计

{{ architecture_overview | default("架构概述待补充。") }}

{% if architecture_diagram %}
![系统架构图]({{ architecture_diagram }})
{% endif %}

## 3.2 "端-边-云"三层架构

{% if architecture_layers %}
{% for layer in architecture_layers %}
### 3.2.{{ loop.index }} {{ layer.layer }}

{{ layer.description }}

**主要组件：**
{% for comp in layer.components %}
- {{ comp }}
{% endfor %}

{% endfor %}
{% else %}
暂无架构层级数据。
{% endif %}

{% if tech_stack %}
## 3.3 技术架构

{{ tech_stack }}
{% endif %}

{% if tech_stack_diagram %}
![技术架构图]({{ tech_stack_diagram }})
{% endif %}

{% if collection_scenario %}
## 3.4 数据采集场景

{{ collection_scenario }}
{% endif %}

{% if collection_scenario_diagram %}
![数据采集场景图]({{ collection_scenario_diagram }})
{% endif %}

{% if network_topology %}
## 3.5 网络架构

{{ network_topology }}
{% endif %}

{% if network_diagram %}
![网络拓扑图]({{ network_diagram }})
{% endif %}

{% if data_flow %}
## 3.6 数据流向

{{ data_flow }}
{% endif %}

{% if security_design %}
## 3.7 安全设计

{{ security_design }}
{% endif %}
