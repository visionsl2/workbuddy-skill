#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物联网解决方案文档生成器 - 主程序
IoT Solution Document Generator

功能：
- 读取YAML格式的方案数据
- 支持Dify知识库查询获取产品信息
- 生成专业Word文档
- 支持多模板切换

使用方法：
    python src/generator.py --project data/projects/example.yaml --template standard --output output/
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import DataLoader
from template_engine import TemplateEngine, SectionRenderer
from doc_builder import DocBuilder
from dify_bridge import DifyBridge


class IoTDocGenerator:
    """物联网解决方案文档生成器"""

    def __init__(self, args):
        self.args = args
        self.base_dir = Path(__file__).parent.parent

        # 初始化数据加载器
        config_path = self.base_dir / "data" / "config.yaml"
        self.loader = DataLoader(str(config_path) if config_path.exists() else None)

        # 初始化Dify（如果配置了）
        if args.dify_api and args.dify_key and args.dify_dataset:
            self.loader.set_dify(args.dify_api, args.dify_key, args.dify_dataset)
        elif args.use_dify:
            # 使用配置文件中的Dify设置
            self.loader.set_dify()

        # 初始化模板引擎
        template_dir = self.base_dir / "templates" / args.template
        self.template_engine = TemplateEngine(str(template_dir))
        self.section_renderer = SectionRenderer(str(template_dir))

        # 加载模板配置
        self.template_config = self._load_template_config(template_dir)

    def _load_template_config(self, template_dir: Path) -> dict:
        """加载模板配置"""
        config_file = template_dir / "template.yaml"
        if config_file.exists():
            return self.loader.load_yaml(str(config_file))
        return {}

    def generate(self):
        """生成文档"""
        print("=" * 50)
        print("IoT解决方案文档生成器")
        print("=" * 50)

        # 1. 加载项目数据
        print(f"\n[1/5] 加载项目数据...")
        project_data = self.loader.load_project(self.args.project)

        # 应用命令行覆盖
        if self.args.override:
            project_data = self.loader.apply_overrides(project_data, self.args.override)
            print(f"  - 应用了 {len(self.args.override)} 个覆盖参数")

        # 扁平化数据用于模板
        context = self.loader.flatten_for_template(project_data)

        # 2. 准备文档构建器
        print(f"\n[2/5] 初始化文档构建器...")
        builder = DocBuilder()

        # 添加封面
        print(f"  - 生成封面...")
        builder.add_cover(context)

        # 添加目录
        print(f"  - 生成目录...")
        builder.add_toc()

        # 3. 渲染各章节
        print(f"\n[3/5] 渲染章节内容...")

        sections = self.template_config.get('sections', [])

        for section in sections:
            if not section.get('enabled', True):
                continue

            section_id = section['id']
            print(f"  - 渲染章节: {section.get('title', section_id)}")

            # 分页
            if section.get('page_break_before', False):
                builder.add_page_break()

            # 获取章节配置
            config_file = section.get('config_file')
            section_config = {}

            if config_file:
                section_path = self.base_dir / "templates" / self.args.template / config_file
                if section_path.exists():
                    section_config = self.loader.load_yaml(str(section_path))

            # 从Dify知识库补充数据
            if self.loader.dify:
                context = self.loader.enrich_from_dify(context, section_config)

            # 渲染Markdown内容
            content_template = section.get('content_template')
            if content_template:
                try:
                    rendered = self.template_engine.render_file(content_template, context)
                    builder.render_markdown(rendered)
                except Exception as e:
                    print(f"    [WARN] 渲染失败: {e}")
                    # 使用简化渲染
                    builder.add_heading1(section.get('title', section_id))
                    builder.add_paragraph(f"[请手动填写 {section_id} 内容]")
            else:
                # 无内容模板，只添加标题
                builder.add_heading1(section.get('title', section_id))

        # 4. 保存文档
        print(f"\n[4/5] 保存文档...")

        # 确保输出目录存在
        output_dir = Path(self.args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        project_name = context.get('project_name', '物联网解决方案')
        version = context.get('document_version', 'V1.0')
        version = version.replace('.', '').replace('V', 'V')

        filename = f"{project_name}_{version}.docx"
        output_path = output_dir / filename

        builder.save(str(output_path))

        # 5. 完成
        print(f"\n[5/5] 完成!")
        print("-" * 50)
        print(f"输出文件: {output_path}")
        print("-" * 50)

        return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='物联网解决方案文档生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用本地数据生成
  python src/generator.py --project data/projects/example.yaml --template standard --output output/

  # 使用Dify知识库
  python src/generator.py --project data/projects/example.yaml --template standard --use-dify --output output/

  # 指定Dify配置
  python src/generator.py --project data/projects/example.yaml --dify-api http://160.0.6.9/v1 --dify-key xxx --dify-dataset xxx --output output/

  # 覆盖特定字段
  python src/generator.py --project data/projects/example.yaml --override "meta.client_name=新客户" --override "overview=新内容" --output output/
        """
    )

    parser.add_argument('--project', '-p', required=True,
                        help='项目数据文件路径 (YAML/JSON)')
    parser.add_argument('--template', '-t', default='standard',
                        help='模板名称 (默认: standard)')
    parser.add_argument('--output', '-o', default='output',
                        help='输出目录 (默认: output)')
    parser.add_argument('--use-dify', action='store_true',
                        help='使用Dify知识库增强数据')
    parser.add_argument('--dify-api',
                        help='Dify API地址')
    parser.add_argument('--dify-key',
                        help='Dify API密钥')
    parser.add_argument('--dify-dataset',
                        help='Dify数据集ID')
    parser.add_argument('--override', '-O', action='append',
                        help='覆盖字段，格式: key.subkey=value')

    args = parser.parse_args()

    # 验证项目文件存在
    if not Path(args.project).exists():
        print(f"[ERROR] 项目文件不存在: {args.project}")
        sys.exit(1)

    # 生成文档
    generator = IoTDocGenerator(args)
    output_file = generator.generate()

    print(f"\n文档生成完成: {output_file}")


if __name__ == '__main__':
    main()
