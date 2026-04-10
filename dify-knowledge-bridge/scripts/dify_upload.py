#!/usr/bin/env python3
"""
Dify 知识库文档上传工具
支持批量上传文件到指定知识库
"""

import os
import sys
import json
import requests

# 配置信息
DIFY_ENDPOINT = "http://160.0.6.9/v1"
DIFY_API_KEY = "dataset-GeVY5VrH2Uu0cgr931oLHaze"
DATASET_ID = "9c3e5075-386d-49cf-a500-b92705eccdf7"


def upload_file_to_dify(file_path: str) -> dict:
    """上传文件到 Dify 知识库"""
    url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/document/create_by_file"

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}"
    }

    data = {
        "indexing_technique": "high_quality",
        "process_rule": json.dumps({
            "mode": "automatic",
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": False}
                ],
                "segment": {
                    "max_tokens": 500,
                    "overlap": 50
                }
            }
        })
    }

    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            print(f"正在上传: {os.path.basename(file_path)}")
            response = requests.post(
                url, headers=headers, files=files, data=data, timeout=120
            )
        return response.json()
    except FileNotFoundError:
        return {"error": f"文件未找到: {file_path}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"上传失败: {str(e)}"}


def upload_text_to_dify(name: str, text: str) -> dict:
    """上传纯文本到 Dify 知识库"""
    url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/document/create_by_text"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "text": text,
        "indexing_technique": "high_quality",
        "process_rule": {"mode": "automatic"}
    }
    try:
        print(f"正在上传文本: {name}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"上传失败: {str(e)}"}


def check_document_status(batch_id: str) -> dict:
    """检查文档处理状态"""
    url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/documents/{batch_id}"
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"查询失败: {str(e)}"}


def list_documents() -> dict:
    """列出知识库中的所有文档"""
    url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/documents"
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"查询失败: {str(e)}"}


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python dify_upload.py <文件路径>   # 上传单个文件")
        print("  python dify_upload.py list         # 列出所有文档")
        print("  python dify_upload.py status <id>  # 检查处理状态")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list":
        result = list_documents()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif command == "status" and len(sys.argv) >= 3:
        result = check_document_status(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 - {file_path}")
            sys.exit(1)
        result = upload_file_to_dify(file_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
