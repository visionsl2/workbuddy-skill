"""
Dify 知识库文档上传工具
通过文件上传方式上传到知识库
"""
import requests
import json
import time
import os

# ============== 配置区 ==============
DIFY_ENDPOINT = "http://160.0.6.9/v1"
API_KEY = "dataset-GeVY5VrH2Uu0cgr931oLHaze"
DATASET_ID = "9c3e5075-386d-49cf-a500-b92705eccdf7"
# ===================================

def upload_file_to_knowledge_base(file_path: str) -> dict:
    """上传文件到知识库"""
    
    url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/documents/upload"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 文件名作为索引名称
    file_name = os.path.basename(file_path)
    
    payload = {
        "indexing_technique": "high_quality",
        "process_rule": {
            "mode": "automatic",
            "rules": {}
        },
        "doc_form": "text_model",
        "doc_language": "Chinese"
    }
    
    print(f"📤 正在上传文件: {file_name}")
    print(f"   目标知识库: {DATASET_ID}")
    
    with open(file_path, 'rb') as f:
        files = {
            "file": (file_name, f, "text/markdown")
        }
        response = requests.post(url, headers=headers, data=payload, files=files)
    
    if response.status_code != 200:
        print(f"❌ 上传失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None
    
    result = response.json()
    print(f"✅ 文件上传成功!")
    
    if 'document' in result:
        doc_info = result['document']
        print(f"   Document ID: {doc_info.get('id')}")
        print(f"   Task ID: {result.get('task_id')}")
        return result
    elif 'documents' in result:
        # 批量上传返回的是数组
        docs = result['documents']
        print(f"   上传了 {len(docs)} 个文档")
        for doc in docs:
            print(f"   - ID: {doc.get('id')}, 名称: {doc.get('name')}")
        return result
    else:
        print(f"响应: {result}")
        return result

def check_indexing_status(document_id: str) -> dict:
    """检查文档索引状态"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    status_url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/documents/{document_id}/indexing-status"
    
    print(f"\n⏳ 等待文档索引...")
    for i in range(30):
        try:
            response = requests.get(status_url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                
                # 检查不同的状态字段格式
                index_status = None
                completed_at = None
                
                # 尝试不同的响应格式
                if isinstance(result, dict):
                    # 可能是 { "id": "...", "indexing_status": "..." }
                    index_status = result.get("indexing_status")
                    
                    # 或者 { "data": [...], "total": ... }
                    if "data" in result and isinstance(result["data"], list):
                        for item in result["data"]:
                            if item.get("id") == document_id:
                                index_status = item.get("indexing_status")
                                completed_at = item.get("completed_at")
                                break
                
                if index_status == "completed":
                    print(f"✅ 索引完成!")
                    return result
                elif index_status == "failed":
                    print(f"❌ 索引失败: {result}")
                    return result
                elif index_status == "in_progress":
                    print(f"   正在索引中... ({i+1}/30s)")
                else:
                    print(f"   状态: {index_status}... ({i+1}/30s)")
            
            time.sleep(1)
        except Exception as e:
            print(f"   检查状态出错: {e}")
            time.sleep(1)
    
    print(f"⚠️ 等待超时，文档可能在后台继续处理")
    return None

def main():
    # 会议纪要文件路径
    file_path = r"C:\SL\中设智控\公司本部\会议纪要\纪要_02-26 内部会议_ 2026经营策略与AI赋能.md"
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    # 上传文件
    result = upload_file_to_knowledge_base(file_path)
    
    if result:
        print(f"\n🎉 上传完成!")
        print(f"📄 文档: 纪要_02-26 内部会议_2026经营策略与AI赋能.md")
        print(f"📚 已收录到知识库: 9c3e5075-386d-49cf-a500-b92705eccdf7 (中设云知识库)")
        
        # 尝试获取文档 ID
        doc_id = None
        if 'document' in result:
            doc_id = result['document'].get('id')
        elif 'documents' in result:
            doc_id = result['documents'][0].get('id') if result['documents'] else None
        
        if doc_id:
            print(f"🆔 Document ID: {doc_id}")
    else:
        print(f"\n❌ 上传失败")

if __name__ == "__main__":
    main()
