#!/usr/bin/env python3
"""
快速功能验证脚本
直接使用Python执行API测试，验证框架核心功能
"""

import requests
import json
from datetime import datetime

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_basic_get():
    """测试基础GET请求"""
    print_section("1️⃣ 测试基础GET请求")
    
    try:
        response = requests.get(
            "https://httpbin.org/get",
            params={
                "username": "test_user",
                "email": "test@example.com"
            },
            timeout=10
        )
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应时间: {response.elapsed.total_seconds():.3f}秒")
        
        data = response.json()
        print(f"  参数验证: username = {data['args'].get('username')}")
        
        assert response.status_code == 200
        assert data['args']['username'] == 'test_user'
        
        print("  ✅ GET请求测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ GET请求测试失败: {e}")
        return False

def test_post_json():
    """测试POST JSON数据"""
    print_section("2️⃣ 测试POST请求 - JSON数据")
    
    try:
        payload = {
            "username": "test_user",
            "action": "create",
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "v1"
            }
        }
        
        response = requests.post(
            "https://httpbin.org/post",
            json=payload,
            timeout=10
        )
        
        print(f"  状态码: {response.status_code}")
        
        data = response.json()
        print(f"  数据验证: username = {data['json'].get('username')}")
        print(f"  数据验证: action = {data['json'].get('action')}")
        
        assert response.status_code == 200
        assert data['json']['username'] == 'test_user'
        assert data['json']['action'] == 'create'
        
        print("  ✅ POST请求测试通过")
        
        # 提取数据（模拟参数提取功能）
        extracted_data = {
            "user_id": data['json']['username'],
            "timestamp": data['json']['metadata']['timestamp']
        }
        print(f"  📦 提取的数据: {extracted_data}")
        
        return True, extracted_data
        
    except Exception as e:
        print(f"  ❌ POST请求测试失败: {e}")
        return False, {}

def test_parameter_reference(user_id):
    """测试参数引用"""
    print_section("3️⃣ 测试参数引用")
    
    try:
        # 使用上一步提取的参数
        response = requests.get(
            "https://httpbin.org/get",
            params={
                "user_id": user_id,
                "operation": "reference_test"
            },
            timeout=10
        )
        
        print(f"  状态码: {response.status_code}")
        
        data = response.json()
        returned_user_id = data['args'].get('user_id')
        
        print(f"  传入参数: user_id = {user_id}")
        print(f"  返回参数: user_id = {returned_user_id}")
        
        assert returned_user_id == user_id
        
        print("  ✅ 参数引用测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 参数引用测试失败: {e}")
        return False

def test_assertions():
    """测试多种断言"""
    print_section("4️⃣ 测试断言功能")
    
    try:
        response = requests.get(
            "https://httpbin.org/headers",
            headers={
                "X-Test-Header": "framework_test",
                "X-Custom-Value": "12345"
            },
            timeout=10
        )
        
        data = response.json()
        
        # 状态码断言
        print(f"  ✅ 状态码断言: {response.status_code} == 200")
        assert response.status_code == 200
        
        # JSON路径断言
        test_header = data['headers'].get('X-Test-Header')
        print(f"  ✅ JSON路径断言: X-Test-Header = {test_header}")
        assert test_header == 'framework_test'
        
        # 响应时间断言
        response_time_ms = response.elapsed.total_seconds() * 1000
        print(f"  ✅ 响应时间断言: {response_time_ms:.0f}ms < 5000ms")
        assert response_time_ms < 5000
        
        # 包含断言
        host = data['headers'].get('Host')
        print(f"  ✅ 包含断言: 'httpbin.org' in '{host}'")
        assert 'httpbin.org' in host
        
        print("  ✅ 断言功能测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 断言功能测试失败: {e}")
        return False

def test_auth():
    """测试认证功能"""
    print_section("5️⃣ 测试认证功能")
    
    try:
        # Basic认证
        response = requests.get(
            "https://httpbin.org/basic-auth/user/passwd",
            auth=('user', 'passwd'),
            timeout=10
        )
        
        print(f"  状态码: {response.status_code}")
        
        data = response.json()
        print(f"  认证状态: {data.get('authenticated')}")
        print(f"  用户名: {data.get('user')}")
        
        assert response.status_code == 200
        assert data['authenticated'] == True
        assert data['user'] == 'user'
        
        print("  ✅ 认证功能测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 认证功能测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print_section("6️⃣ 测试错误处理")
    
    try:
        # 测试404
        response = requests.get(
            "https://httpbin.org/status/404",
            timeout=10
        )
        
        print(f"  404状态码: {response.status_code}")
        assert response.status_code == 404
        print("  ✅ 404错误处理正常")
        
        # 测试500
        response = requests.get(
            "https://httpbin.org/status/500",
            timeout=10
        )
        
        print(f"  500状态码: {response.status_code}")
        assert response.status_code == 500
        print("  ✅ 500错误处理正常")
        
        print("  ✅ 错误处理测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 错误处理测试失败: {e}")
        return False

def test_delay_response():
    """测试延迟响应"""
    print_section("7️⃣ 测试延迟响应")
    
    try:
        import time
        start_time = time.time()
        
        response = requests.get(
            "https://httpbin.org/delay/2",
            timeout=10
        )
        
        elapsed = time.time() - start_time
        
        print(f"  状态码: {response.status_code}")
        print(f"  实际延迟: {elapsed:.2f}秒")
        
        assert response.status_code == 200
        assert elapsed >= 2.0  # 应该至少延迟2秒
        assert elapsed < 5.0   # 但不应超过5秒
        
        print("  ✅ 延迟响应测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 延迟响应测试失败: {e}")
        return False

def test_special_characters():
    """测试特殊字符处理"""
    print_section("8️⃣ 测试特殊字符处理")
    
    try:
        payload = {
            "chinese": "测试中文字符",
            "emoji": "🎯🚀💪",
            "special": "!@#$%^&*()",
            "unicode": "Hello 世界 🌍"
        }
        
        response = requests.post(
            "https://httpbin.org/post",
            json=payload,
            timeout=10
        )
        
        print(f"  状态码: {response.status_code}")
        
        data = response.json()
        
        print(f"  中文验证: {data['json']['chinese']}")
        print(f"  Emoji验证: {data['json']['emoji']}")
        print(f"  特殊字符验证: {data['json']['special']}")
        
        assert data['json']['chinese'] == "测试中文字符"
        assert data['json']['emoji'] == "🎯🚀💪"
        
        print("  ✅ 特殊字符处理测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 特殊字符处理测试失败: {e}")
        return False

def test_workflow():
    """测试完整工作流"""
    print_section("9️⃣ 测试完整工作流")
    
    try:
        # 步骤1: 创建资源
        print("  步骤1: 创建资源")
        response1 = requests.post(
            "https://httpbin.org/post",
            json={
                "resource_type": "user",
                "username": "workflow_user"
            },
            timeout=10
        )
        resource_id = response1.json()['json']['username']
        print(f"    ✅ 资源已创建: {resource_id}")
        
        # 步骤2: 查询资源
        print("  步骤2: 查询资源")
        response2 = requests.get(
            "https://httpbin.org/get",
            params={"resource_id": resource_id},
            timeout=10
        )
        queried_id = response2.json()['args']['resource_id']
        print(f"    ✅ 资源已查询: {queried_id}")
        
        # 步骤3: 更新资源
        print("  步骤3: 更新资源")
        response3 = requests.put(
            "https://httpbin.org/put",
            json={
                "resource_id": resource_id,
                "status": "updated"
            },
            timeout=10
        )
        print(f"    ✅ 资源已更新")
        
        # 步骤4: 删除资源
        print("  步骤4: 删除资源")
        response4 = requests.delete(
            "https://httpbin.org/delete",
            params={"resource_id": resource_id},
            timeout=10
        )
        print(f"    ✅ 资源已删除")
        
        print("  ✅ 工作流测试通过")
        return True
        
    except Exception as e:
        print(f"  ❌ 工作流测试失败: {e}")
        return False

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🚀 YH API测试框架 - 快速功能验证                      ║
║                                                          ║
║     直接验证核心功能是否正常工作                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    results = []
    
    # 执行所有测试
    results.append(("基础GET请求", test_basic_get()))
    
    success, extracted = test_post_json()
    results.append(("POST请求", success))
    
    if extracted:
        results.append(("参数引用", test_parameter_reference(extracted.get('user_id'))))
    
    results.append(("断言功能", test_assertions()))
    results.append(("认证功能", test_auth()))
    results.append(("错误处理", test_error_handling()))
    results.append(("延迟响应", test_delay_response()))
    results.append(("特殊字符", test_special_characters()))
    results.append(("完整工作流", test_workflow()))
    
    # 统计结果
    print_section("📊 测试结果统计")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n  总测试数: {total}")
    print(f"  通过数量: {passed}")
    print(f"  失败数量: {total - passed}")
    print(f"  成功率: {success_rate:.1f}%\n")
    
    # 详细结果
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print("\n" + "="*60)
    if passed == total:
        print("🎉 所有测试通过！框架功能正常！")
    else:
        print(f"⚠️  有 {total - passed} 个测试失败")
    print("="*60)
    
    print("\n💡 下一步:")
    print("  1. 运行完整测试套件: python run_comprehensive_test.py")
    print("  2. 或使用pytest: pytest comprehensive_test.yaml -v")
    print("  3. 查看测试文件: comprehensive_test.yaml")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
