{# 产品选型清单模板 - Product List Template #}

# 4. 产品选型清单

{{ introduction | default("以下为推荐的核心产品选型清单：") }}

{% if categories %}
{% for category in categories %}
## 4.{{ loop.index }} {{ category.category_name }}

| 产品名称 | 型号 | 厂商 | 数量 | 单位 | 关键参数 |
|:---------|:-----|:-----|:----:|:----:|:---------|
{% for product in category.products %}
| {{ product.name }} | {{ product.model }} | {{ product.manufacturer }} | {{ product.quantity }} | {{ product.unit }} | {{ product.key_params }} |
{% endfor %}

{% endfor %}
{% else %}
暂无产品数据。
{% endif %}
