"""
Dify 知识库文档上传工具
通过 API 直接上传文本内容到知识库

用法:
    python upload_to_kb.py "文件路径" [知识库ID]
    
示例:
    python upload_to_kb.py "C:\\文档\\会议纪要.md"
    python upload_to_kb.py "C:\\文档\\会议纪要.md" "9c3e5075-..."
"""
import requests
import sys
import time
import os

# ============== 配置区 ==============
DIFY_ENDPOINT = "http://160.0.6.9/v1"
API_KEY = "dataset-GeVY5VrH2Uu0cgr931oLHaze"
DEFAULT_DATASET_ID = "9c3e5075-386d-49cf-a500-b92705eccdf7"  # 中设云知识库
# =====================================

def upload_document(file_path: str, dataset_id: str = None, wait: bool = True) -> dict:
    """上传文档到知识库"""
    
    if dataset_id is None:
        dataset_id = DEFAULT_DATASET_ID
    
    # 读取文件内容
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成文档名称（使用文件名）
    doc_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 正确的 API 路径：document (单数!)
    url = f"{DIFY_ENDPOINT}/datasets/{dataset_id}/document/create-by-text"
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'name': doc_name,
        'text': content,
        'indexing_technique': 'high_quality',
        'doc_form': 'text_model',
        'doc_language': 'Chinese',
        'process_rule': {
            'mode': 'automatic'
        }
    }
    
    print(f"[UPLOAD] {doc_name}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        doc = result.get('document', {})
        doc_id = doc.get('id')
        batch_id = result.get('batch')
        
        print(f"[OK] Document ID: {doc_id}")
        
        if wait:
            print("[...] Waiting for indexing...")
            wait_for_indexing(dataset_id, doc_id)
        
        return result
    else:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")

def wait_for_indexing(dataset_id: str, doc_id: str, timeout: int = 60):
    """等待文档索引完成"""
    headers = {'Authorization': f'Bearer {API_KEY}'}
    url = f"{DIFY_ENDPOINT}/datasets/{dataset_id}/documents/{doc_id}/indexing-status"
    
    for i in range(timeout // 2):
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            result = resp.json()
            status = result.get('indexing_status', 'unknown')
            print(f"  [{i*2}s] {status}")
            
            if status == 'completed':
                print("[SUCCESS] Indexing completed!")
                return True
            elif status == 'error':
                print("[ERROR] Indexing failed!")
                return False
        
        time.sleep(2)
    
    print("[TIMEOUT] Still processing in background")
    return False

def list_documents(dataset_id: str = None):
    """列出知识库中的文档"""
    if dataset_id is None:
        dataset_id = DEFAULT_DATASET_ID
    
    headers = {'Authorization': f'Bearer {API_KEY}'}
    url = f"{DIFY_ENDPOINT}/datasets/{dataset_id}/documents"
    
    resp = requests.get(url, headers=headers)
    
    if resp.status_code == 200:
        result = resp.json()
        docs = result.get('data', [])
        print(f"Knowledge Base: {len(docs)} documents")
        for doc in docs:
            name = doc.get('name', 'N/A')
            status = doc.get('indexing_status', 'unknown')
            print(f"  - {name} [{status}]")
    else:
        print(f"Error: {resp.status_code}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_to_kb.py <file_path> [dataset_id]")
        print()
        print("Examples:")
        print('  python upload_to_kb.py "C:\\文档\\会议纪要.md"')
        print('  python upload_to_kb.py "C:\\文档\\会议纪要.md" "9c3e5075-..."')
        print()
        list_documents()
        return
    
    file_path = sys.argv[1]
    dataset_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        upload_document(file_path, dataset_id)
        print()
        print("Done!")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
