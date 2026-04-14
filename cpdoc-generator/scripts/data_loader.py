#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载器 - Data Loader
负责加载和合并多数据源：本地YAML/JSON文件、Dify知识库、命令行覆盖
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dify_bridge import DifyBridge


class DataLoader:
    """多数据源数据加载器"""

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.dify = None

    def _load_config(self, config_path: str = None) -> Dict:
        """加载全局配置"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "data" / "config.yaml"

        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def load_yaml(self, file_path: str) -> Dict:
        """加载YAML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_json(self, file_path: str) -> Dict:
        """加载JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_project(self, project_path: str) -> Dict:
        """加载项目数据文件"""
        path = Path(project_path)
        if not path.exists():
            raise FileNotFoundError(f"项目文件不存在: {project_path}")

        if path.suffix in ['.yaml', '.yml']:
            return self.load_yaml(project_path)
        elif path.suffix == '.json':
            return self.load_json(project_path)
        else:
            raise ValueError(f"不支持的文件格式: {path.suffix}")

    def set_dify(self, api_base: str = None, api_key: str = None, dataset_id: str = None):
        """设置Dify连接"""
        config = self.config.get('dify', {})

        self.dify = DifyBridge(
            api_base=api_base or config.get('api_base'),
            api_key=api_key or config.get('api_key'),
            dataset_id=dataset_id or config.get('dataset_id')
        )

    def query_dify(self, query: str, top_k: int = 3) -> List[Dict]:
        """查询Dify知识库"""
        if not self.dify:
            return []
        return self.dify.query(query, top_k)

    def enrich_from_dify(self, data: Dict, section_config: Dict) -> Dict:
        """根据章节配置从Dify知识库补充数据"""
        if not section_config.get('data_mapping'):
            return data

        enriched = data.copy()
        data_mapping = section_config.get('data_mapping', {})

        for field_name, field_config in data_mapping.items():
            source = field_config.get('source', '')

            # 检查是否需要从Dify获取
            if field_config.get('dify_query'):
                # 检查本地是否有数据
                local_value = self._get_nested(data, source)

                if not local_value or local_value == field_config.get('default'):
                    # 从Dify查询
                    query = field_config['dify_query']
                    results = self.query_dify(query)

                    if results:
                        # 提取Dify返回的文本
                        texts = [r.get('text', '') for r in results]
                        enriched[field_name] = texts[0] if texts else None

        return enriched

    def _get_nested(self, data: Dict, key_path: str) -> Any:
        """获取嵌套字典的值"""
        keys = key_path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value

    def merge_data(self, base_data: Dict, override_data: Dict) -> Dict:
        """合并数据，override_data优先"""
        result = base_data.copy()

        for key, value in override_data.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_data(result[key], value)
            else:
                result[key] = value

        return result

    def apply_overrides(self, data: Dict, overrides: List[str]) -> Dict:
        """应用命令行覆盖参数

        Args:
            data: 原始数据
            overrides: 覆盖参数列表，格式如 "key.subkey=value"
        """
        result = data.copy()

        for override in overrides:
            if '=' not in override:
                continue

            key_path, value = override.split('=', 1)
            key_path = key_path.strip()
            value = value.strip()

            # 设置嵌套值
            keys = key_path.split('.')
            current = result

            for i, key in enumerate(keys[:-1]):
                if key not in current:
                    current[key] = {}
                current = current[key]

            current[keys[-1]] = value

        return result

    def flatten_for_template(self, data: Dict) -> Dict:
        """将嵌套数据扁平化，方便模板引用

        例如：
        {
            "meta": {"project_name": "xxx"},
            "executive_summary": {"overview": "yyy"},
            "architecture_overview": "xxx"  # 顶层字段也会被保留
        }

        转换为：
        {
            "project_name": "xxx",
            "overview": "yyy",
            "architecture_overview": "xxx",  # 顶层字段保留
            "data": data  # 保留原始嵌套结构
        }
        """
        flat = {}

        # 遍历所有顶层键值对
        for key, value in data.items():
            if isinstance(value, dict):
                # 嵌套字典：扁平化一级
                for sub_key, sub_value in value.items():
                    flat[sub_key] = sub_value
            elif isinstance(value, list):
                # 列表：保留原样
                flat[key] = value
            else:
                # 基础类型（字符串、数字等）：直接保留
                flat[key] = value

        # 保留原始数据（用于复杂结构引用）
        flat['data'] = data
        flat['_meta'] = data.get('meta', {})

        # 提取元信息到顶层（覆盖同名字段）
        meta = data.get('meta', {})
        for key, value in meta.items():
            flat[key] = value

        return flat


def main():
    """测试数据加载器"""
    loader = DataLoader()

    # 测试加载示例项目
    project_path = Path(__file__).parent.parent / "data" / "projects" / "example.yaml"
    data = loader.load_project(str(project_path))

    print(f"加载项目: {data['meta']['project_name']}")
    print(f"客户: {data['meta']['client_name']}")
    print(f"产品类别数: {len(data['product_list']['categories'])}")


if __name__ == '__main__':
    main()
