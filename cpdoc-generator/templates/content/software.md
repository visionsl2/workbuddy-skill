# 5. 平台方案设计

本章包含两部分内容：定制化项目需求设计和标准平台功能介绍。

## 5.1 项目需求设计

{% for module in software_modules %}
### {{ module.title }}

{{ module.description }}

{% endfor %}

---

## 5.2 中设CPIOT平台介绍

{% for module in platform_modules %}
### {{ module.title }}

{{ module.description }}

{% if module.image %}
![{{ module.title }}]({{ module.image }})
{% endif %}
{% if module.image1 %}
![{{ module.title }}-1]({{ module.image1 }})
{% endif %}
{% if module.image2 %}
![{{ module.title }}-2]({{ module.image2 }})
{% endif %}
{% if module.image3 %}
![{{ module.title }}-3]({{ module.image3 }})
{% endif %}
{% if module.image4 %}
![{{ module.title }}-4]({{ module.image4 }})
{% endif %}
{% if module.image5 %}
![{{ module.title }}-5]({{ module.image5 }})
{% endif %}

{% if module.features %}
{% for feature in module.features %}
- {{ feature }}
{% endfor %}
{% endif %}

{% endfor %}
