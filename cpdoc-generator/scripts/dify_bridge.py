#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify知识库桥接 - Dify Knowledge Bridge
封装Dify API调用，支持产品信息查询和内容检索
"""

import requests
from typing import List, Dict, Optional


class DifyBridge:
    """Dify知识库查询接口"""

    def __init__(self, api_base: str, api_key: str, dataset_id: str):
        """
        Args:
            api_base: Dify API地址，如 http://160.0.6.9/v1
            api_key: API密钥
            dataset_id: 知识库数据集ID
        """
        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.dataset_id = dataset_id
        self.session = None

    def _init_session(self):
        """初始化HTTP会话"""
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })

    def query(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """
        查询知识库

        Args:
            query_text: 查询文本
            top_k: 返回结果数量

        Returns:
            查询结果列表
        """
        self._init_session()

        url = f"{self.api_base}/datasets/{self.dataset_id}/retrieval"

        payload = {
            "query": query_text,
            "retrieval_setting": {
                "top_k": top_k,
                "score_threshold": 0.5
            }
        }

        try:
            response = self.session.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get('records', [])
            else:
                print(f"[WARN] 知识库查询失败: {response.status_code} - {response.text}")
                return []

        except requests.exceptions.ConnectionError:
            print(f"[WARN] 无法连接到Dify服务: {self.api_base}")
            return []
        except Exception as e:
            print(f"[WARN] 知识库查询异常: {e}")
            return []

    def get_product_info(self, product_name: str) -> Optional[Dict]:
        """获取产品详细信息"""
        results = self.query(f"产品参数 规格 {product_name}", top_k=1)

        if results:
            return {
                'name': product_name,
                'description': results[0].get('text', ''),
                'source': results[0].get('doc_id', '')
            }
        return None

    def get_case_info(self, case_name: str) -> Optional[Dict]:
        """获取案例信息"""
        results = self.query(f"成功案例 项目 {case_name}", top_k=1)

        if results:
            return {
                'name': case_name,
                'description': results[0].get('text', '')
            }
        return None

    def enrich_product_list(self, products: List[Dict]) -> List[Dict]:
        """批量补充产品信息"""
        enriched = []

        for product in products:
            name = product.get('name', '')
            if name:
                info = self.get_product_info(name)
                if info and info['description']:
                    product['description_enriched'] = info['description']
            enriched.append(product)

        return enriched


def test_connection(api_base: str, api_key: str, dataset_id: str) -> bool:
    """测试Dify连接"""
    bridge = DifyBridge(api_base, api_key, dataset_id)
    results = bridge.query("测试连接", top_k=1)

    if results:
        print(f"[OK] Dify连接正常，返回 {len(results)} 条结果")
        return True
    else:
        print("[WARN] Dify连接可能异常，未返回结果")
        return False


if __name__ == '__main__':
    import yaml
    from pathlib import Path

    # 加载配置
    config_path = Path(__file__).parent.parent / "data" / "config.yaml"

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        dify_config = config.get('dify', {})

        print(f"测试Dify连接...")
        print(f"API: {dify_config.get('api_base')}")
        print(f"Dataset: {dify_config.get('dataset_id')}")

        test_connection(
            dify_config.get('api_base'),
            dify_config.get('api_key'),
            dify_config.get('dataset_id')
        )
    else:
        print("[ERROR] 配置文件不存在")
