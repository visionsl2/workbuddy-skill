#!/usr/bin/env python3
"""
测试 Dify 知识库连接
"""

import json
import sys
import requests
import os

def load_config():
    """加载配置文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "dify_mcp_config.json")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("配置文件 dify_mcp_config.json 未找到")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {e}")
        sys.exit(1)

def test_connection():
    """测试 Dify 连接"""
    config = load_config()

    endpoint = config.get("dify_endpoint", "")
    api_key = config.get("dify_api_key", "")

    print("=" * 50)
    print("Dify 知识库连接测试")
    print("=" * 50)

    # 测试 health
    try:
        health_url = endpoint.replace("/v1", "/health")
        resp = requests.get(health_url, timeout=5)
        print(f"Health Check: {resp.status_code} - OK" if resp.status_code == 200 else f"Health Check: {resp.status_code}")
    except Exception as e:
        print(f"Health Check: 失败 - {e}")

    # 测试检索
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"knowledge_id": config.get("knowledge_id", ""), "query": "测试", "retrieval_setting": {"top_k": 1, "score_threshold": 0.5}}
        resp = requests.post(f"{endpoint}/retrieval", headers=headers, json=payload, timeout=10)
        print(f"检索测试: {resp.status_code}")
        if resp.status_code == 200:
            print("连接成功！")
        else:
            print(f"错误: {resp.text}")
    except Exception as e:
        print(f"检索测试: 失败 - {e}")

if __name__ == "__main__":
    test_connection()
