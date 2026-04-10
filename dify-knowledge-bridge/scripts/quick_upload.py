import requests
import os

file_path = r'C:\SL\中设智控\公司本部\会议纪要\纪要_02-26 内部会议_ 2026经营策略与AI赋能.md'
dataset_id = '9c3e5075-386d-49cf-a500-b92705eccdf7'
api_key = 'dataset-GeVY5VrH2Uu0cgr931oLHaze'
endpoint = 'http://160.0.6.9/v1'

print('='*50)
print('Dify Knowledge Base Upload')
print('='*50)
print(f'File: {file_path}')
print(f'File exists: {os.path.exists(file_path)}')

if os.path.exists(file_path):
    print(f'File size: {os.path.getsize(file_path)} bytes')
else:
    print('[ERROR] File not found!')
    exit(1)

print()
print('[UPLOAD] Starting...')
url = f'{endpoint}/datasets/{dataset_id}/documents/upload'
headers = {'Authorization': f'Bearer {api_key}'}

with open(file_path, 'rb') as f:
    files = {'file': (os.path.basename(file_path), f, 'text/markdown')}
    response = requests.post(url, headers=headers, files=files)

print()
print(f'Status: {response.status_code}')
print()

if response.status_code in [200, 201]:
    print('[SUCCESS] Upload completed!')
    result = response.json()
    print(result)
    print()
    print('Document added to knowledge base!')
else:
    print('[ERROR] Upload failed!')
    print(response.text[:1000])
