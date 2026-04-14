#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板引擎 - Template Engine
使用Jinja2处理Markdown内容模板
"""

import re
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound


class TemplateEngine:
    """Jinja2模板引擎封装"""

    def __init__(self, template_dir: str):
        """
        Args:
            template_dir: 模板目录路径
        """
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # 添加自定义过滤器
        self.env.filters['default'] = self._custom_default

    def _custom_default(self, value, default_value=''):
        """自定义default过滤器"""
        if value is None or value == '':
            return default_value
        return value

    def render_file(self, template_path: str, context: Dict[str, Any]) -> str:
        """
        渲染模板文件

        Args:
            template_path: 模板文件相对路径（相对于template_dir）
            context: 渲染上下文数据

        Returns:
            渲染后的字符串
        """
        try:
            template = self.env.get_template(template_path)
            return template.render(**context)
        except TemplateNotFound:
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

    def render_string(self, template_str: str, context: Dict[str, Any]) -> str:
        """
        渲染模板字符串

        Args:
            template_str: 模板字符串
            context: 渲染上下文数据

        Returns:
            渲染后的字符串
        """
        template = Template(template_str)
        return template.render(**context)

    def load_section_template(self, template_name: str) -> str:
        """加载章节模板内容"""
        template_path = f"content/{template_name}.md"
        return self.render_file(template_path, {})

    def parse_yaml_config(self, config_path: str) -> Dict:
        """加载YAML配置"""
        import yaml

        full_path = self.template_dir / config_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def get_template_vars(self, template_path: str) -> set:
        """
        提取模板中的变量名

        Args:
            template_path: 模板文件路径

        Returns:
            变量名集合
        """
        try:
            template = self.env.get_template(template_path)
            source = template.source

            # 提取 {{ var }} 和 {{ var.name }} 格式
            patterns = [
                r'\{\{\s*(\w+)\s*\}\}',  # {{ var }}
                r'\{\{\s*(\w+)\.\w+\s*\}\}',  # {{ var.name }}
            ]

            vars = set()
            for pattern in patterns:
                matches = re.findall(pattern, source)
                vars.update(matches)

            return vars
        except Exception:
            return set()


class SectionRenderer:
    """章节渲染器"""

    def __init__(self, template_dir: str):
        self.engine = TemplateEngine(template_dir)

    def render_section(self, section_config: Dict, data: Dict) -> str:
        """
        渲染单个章节

        Args:
            section_config: 章节配置（包含content_template路径）
            data: 数据上下文

        Returns:
            渲染后的Markdown文本
        """
        content_template = section_config.get('content_template')
        if not content_template:
            return ""

        # 准备上下文：扁平化数据 + 原始数据
        context = data.copy() if isinstance(data, dict) else {}

        # 添加常用别名
        if 'data' in context:
            nested = context['data']
            for key, value in nested.items():
                if key not in context:
                    context[key] = value

        return self.engine.render_file(content_template, context)


def test_engine():
    """测试模板引擎"""
    template_dir = Path(__file__).parent.parent / "templates" / "standard"
    engine = TemplateEngine(str(template_dir))

    # 测试渲染
    test_data = {
        'project_name': '测试项目',
        'client_name': '测试客户',
        'overview': '这是测试概述',
        'key_benefits': ['效益1', '效益2', '效益3']
    }

    result = engine.render_file('content/overview.md', test_data)
    print("渲染结果:")
    print(result)


if __name__ == '__main__':
    test_engine()
