"""
Dify 知识库文档上传工具
直接通过文本内容上传到指定知识库
"""
import requests
import json
import time

# ============== 配置区 ==============
DIFY_ENDPOINT = "http://160.0.6.9/v1"
API_KEY = "dataset-GeVY5VrH2Uu0cgr931oLHaze"
DATASET_ID = "9c3e5075-386d-49cf-a500-b92705eccdf7"
# ===================================

def upload_text_to_knowledge_base(title: str, content: str) -> dict:
    """上传文本内容到知识库"""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Step 1: 创建文档
    create_url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/documents"
    payload = {
        "indexing_technique": "high_quality",
        "process_rule": {
            "mode": "automatic",
            "rules": {}
        },
        "doc_form": "text_model",
        "doc_language": "Chinese",
        "document": {
            "title": title,
            "text": content
        }
    }
    
    print(f"📤 正在创建文档: {title}")
    response = requests.post(create_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"❌ 创建文档失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None
    
    result = response.json()
    print(f"✅ 文档创建成功!")
    print(f"   Document ID: {result.get('document', {}).get('id')}")
    print(f"   Task ID: {result.get('task_id')}")
    
    return result

def check_indexing_status(task_id: str, max_wait: int = 60) -> dict:
    """检查文档索引状态"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    status_url = f"{DIFY_ENDPOINT}/datasets/{DATASET_ID}/documents/{task_id}/indexing-status"
    
    print(f"⏳ 等待文档索引完成...")
    for i in range(max_wait):
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            status = result.get('doc_form', {}).get('indexing_status', 'unknown')
            completed = result.get('doc_form', {}).get('completed_at')
            
            if status == 'completed':
                print(f"✅ 索引完成!")
                return result
            elif status == 'failed':
                print(f"❌ 索引失败: {result}")
                return result
            
            print(f"   状态: {status}... ({i+1}/{max_wait}s)")
        
        time.sleep(1)
    
    print(f"⚠️ 等待超时")
    return None

def main():
    # 会议纪要内容
    content = """# 纪要_02-26 内部会议: 2026经营策略与AI赋能

## 会议概要
主题: 2026战略部署 | 时间: 2026-02-26 15:47:36 | 参与人: 王利攀

会议围绕2026年公司经营战略展开，重点强调AI技术应用、内部管理优化、客户经营深化与市场拓展升级四大方向。

## 一、AI全面赋能与技术革新

核心方向：
- 将AI作为2026年核心技术驱动力，在会议纪要、销售支持、解决方案生成等环节已初步验证其高效性
- 强调AI实时记录能力，指出当前AI工具能精准总结长达一小时的会议要点
- AI不是颠覆者而是加速器，类比高铁取代步行，提升执行速度而非替代人类判断

实施路径：
- 推行"拿来主义+共创+自研"策略：通用型工具直接引入，行业化解决方案与客户联合共创，内部效率工具自主开发
- 要求每月有产出，每项自研聚焦具体场景，如销售助手、售前支持工具等
- "自用加输出相结合"，内部验证有效的AI应用可转化为对外服务产品

## 二、内部管理改革与运营提效

独立核算机制：
- 坚决执行部门自负盈亏与独立核算制度，要求各负责人对项目成本与回款负责
- 财务数据需在工资发放前提交审批，杜绝以往执行打折现象
- 对亏损项目追责，要求负责人自行解决资金问题

组织与资源配置：
- 推动专业化分工与高效协作，打破单兵作战模式，加强跨事业部协同
- 优化人力资源配置，淘汰低效人员，保留优质资源并向高产出领域倾斜
- 销售岗位实行扁平化管理，3月1日起正式实施新组织架构

## 三、客户经营战略升级

客户分类经营：
- 明确将客户分为战略客户、老客户、咨询未成交客户及丢单客户四类
- 战略客户应不少于20家，即使短期无业务也需长期维护
- 丢单客户再跟进成功率更高，多个标杆项目均为原丢单客户转化而来

经营方法论：
- 从被动响应转向主动经营，为客户制定三年行动计划
- 加强客户生命周期管理，针对使用超10年的老系统推动迭代升级
- 利用AI分析客户动态（如股价上涨、投资扩产），及时捕捉业务机会

## 四、市场与品牌重塑计划

市场渠道多元化：
- 打破依赖百度单一渠道的局面，构建"百度+自有媒体"双链路宣传体系
- 聚焦高增长行业精准投放，重点布局半导体、新能源（光伏、风电、储能）等领域
- 拓展合作渠道形态，重点培育类华为系、类起源方等企业级合作伙伴

品牌与IP建设：
- 启动中社品牌复兴计划，恢复在设备资产管理与工业互联网领域的专业影响力
- 策划新产品发布会，推广成熟平台，强化市场认知
- 全员参与品牌传播，每位员工都是公司品牌的代言人

## 五、产品与交付体系升级

产品力提升：
- 成立产品部并尽快运转，统筹推进产品规划与迭代
- 解决"有没有"之后聚焦"好不好"，加快基线版、行业版、创新版解决方案沉淀
- 重点布局AI融合与预测性维护功能

交付效能优化：
- 推进标准化实施落地，打破"吃大锅饭"现象，建立工时定额与绩效挂钩机制
- 借助AI工具提升人效，实现"一个自然人+一个数字人"协同作业模式

## 待办事项
1. 启动AI全面赋能行动计划，包括会议纪要、销售支持、解决方案生成等场景的工具开发与应用
2. 加快产品部组建与运作，推动产品迭代尤其是AI赋能的新能力落地
3. 建立中台解决方案库并利用AI实现高效调用，支撑售前团队快速响应客户需求
4. 开展老客户系统迭代引导工作，针对生命周期后半段系统制定升级应对方案
5. 优化市场宣传策略，精准投放至半导体、新能源等高增长行业
6. 推动官网系项目作为公司级战略项目落地
7. 梳理华为系客户潜在转化机会，力争实现500至1000万元的业务转化
8. 组织制定战略客户经营计划，重点覆盖20家以上战略客户及历史丢单客户的回访与维护
9. 落实部门独立核算制度，确保每月发工资前提交部门核算情况
10. 研究并提出AI在各部门工作环节中的应用方案"""

    title = "纪要_02-26 内部会议_2026经营策略与AI赋能"
    
    # 上传文档
    result = upload_text_to_knowledge_base(title, content)
    
    if result:
        # 检查索引状态
        doc_id = result.get('document', {}).get('id')
        if doc_id:
            status = check_indexing_status(doc_id)
            if status:
                print(f"\n🎉 上传完成!")
                print(f"📄 文档已收录到知识库: {title}")
            else:
                print(f"\n⚠️ 文档已上传，但索引可能需要更长时间")
                print(f"📄 文档标题: {title}")
                print(f"🆔 Document ID: {doc_id}")
    else:
        print(f"\n❌ 上传失败，请检查错误信息")

if __name__ == "__main__":
    main()
