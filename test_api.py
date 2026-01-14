"""
API 测试脚本
用于快速测试道路病害识别接口
"""

import requests
import json
from pathlib import Path


API_BASE = "http://localhost:8000/api"


def test_health():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    response = requests.get(f"{API_BASE}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_detect(image_path: str):
    """测试病害检测"""
    print(f"=== 测试病害检测: {image_path} ===")
    
    if not Path(image_path).exists():
        print(f"错误: 文件不存在 {image_path}")
        return None
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_BASE}/detect", files=files)
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"检测ID: {result['id']}")
        print(f"风险等级: {result['risk_level']}")
        print(f"检测到 {len(result['damages'])} 处病害:")
        
        for i, damage in enumerate(result['damages'], 1):
            print(f"\n病害 {i}:")
            print(f"  类型: {damage['type']}")
            print(f"  严重程度: {damage['severity']}")
            print(f"  位置: {damage['location']}")
            print(f"  尺寸: {damage['size']}")
            print(f"  置信度: {damage['confidence']:.2%}")
            print(f"  建议: {damage['suggestAction']}")
        
        return result['id']
    else:
        print(f"错误: {response.text}")
        return None
    
    print()


def test_feedback(damage_id: str):
    """测试提交修正"""
    print(f"=== 测试提交修正: {damage_id} ===")
    
    feedback_data = {
        "damage_id": damage_id,
        "corrected": {
            "type": "裂缝",
            "severity": "中等",
            "location": "K10+500 左侧车道",
            "size": "100x2x0.5cm"
        }
    }
    
    response = requests.post(
        f"{API_BASE}/feedback",
        json=feedback_data
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_similar(damage_id: str):
    """测试相似病害查询"""
    print(f"=== 测试相似病害查询: {damage_id} ===")
    
    response = requests.get(f"{API_BASE}/similar/{damage_id}")
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"找到 {len(result['similar_cases'])} 个相似案例")
        
        for i, case in enumerate(result['similar_cases'], 1):
            print(f"\n相似案例 {i}:")
            print(f"  ID: {case['id']}")
            print(f"  类型: {case['damage_type']}")
            print(f"  严重程度: {case['severity']}")
            print(f"  时间: {case['created_at']}")
    else:
        print(f"错误: {response.text}")
    
    print()


def test_stats():
    """测试统计数据"""
    print("=== 测试统计数据 ===")
    
    response = requests.get(f"{API_BASE}/stats")
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


if __name__ == "__main__":
    print("道路病害识别 API 测试\n")
    
    # 1. 健康检查
    test_health()
    
    # 2. 病害检测(需要提供图片路径)
    image_path = input("请输入测试图片路径(回车跳过): ").strip()
    
    if image_path:
        damage_id = test_detect(image_path)
        
        if damage_id:
            # 3. 提交修正
            test_feedback(damage_id)
            
            # 4. 查询相似
            test_similar(damage_id)
    
    # 5. 统计数据
    test_stats()
    
    print("测试完成!")
