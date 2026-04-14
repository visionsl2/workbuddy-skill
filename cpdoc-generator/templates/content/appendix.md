{# 附录模板 - Appendix Template #}

## 8. 附录

### 8.1 系统技术规格

{% if technical_specs %}
{% for spec in technical_specs %}
- {{ spec }}
{% endfor %}
{% else %}
- 系统可用性 ≥ 99.9%
- 数据采集延迟 ≤ 1秒
- 支持并发在线设备 ≥ 10000台
{% endif %}

### 8.2 参考标准规范

{% if reference_standards %}
{% for standard in reference_standards %}
- {{ standard }}
{% endfor %}
{% else %}
- GB/T 22239-2019 信息安全技术 网络安全等级保护基本要求
- GB/T 32919-2016 信息安全技术 工业控制系统安全控制应用指南
{% endif %}

### 8.3 企业资质

{% if certifications %}
{% for cert in certifications %}
- {{ cert }}
{% endfor %}
{% else %}
- ISO 9001:2015 质量管理体系认证
- ISO 27001:2022 信息安全管理体系认证
- 高新技术企业认定
{% endif %}

{% if diagrams.certifications %}
### 8.4 资质证书图片

{% for img in diagrams.certifications %}
![资质证书]({{ img }})
{% endfor %}
{% endif %}
