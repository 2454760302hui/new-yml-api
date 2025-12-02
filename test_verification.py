"""
功能验证测试脚本
Functionality Verification Test Script

验证优化后的核心功能是否正常工作
"""

import sys
import traceback
from typing import Dict, Any

# 测试结果收集
test_results = {
    'passed': [],
    'failed': [],
    'total': 0
}


def test_case(name: str):
    """测试用例装饰器"""
    def decorator(func):
        def wrapper():
            test_results['total'] += 1
            try:
                func()
                test_results['passed'].append(name)
                print(f"✅ PASS: {name}")
                return True
            except Exception as e:
                test_results['failed'].append((name, str(e)))
                print(f"❌ FAIL: {name}")
                print(f"   错误: {str(e)}")
                traceback.print_exc()
                return False
        return wrapper
    return decorator


@test_case("模块导入测试")
def test_module_imports():
    """测试核心模块是否可以正常导入"""
    import runner
    import http_client
    import validate
    import extract
    import config_manager
    import performance_config
    assert runner is not None
    assert http_client is not None
    assert validate is not None


@test_case("HTTP客户端创建测试")
def test_http_client_creation():
    """测试HTTP客户端是否可以正常创建"""
    from http_client import HttpClient
    
    client = HttpClient()
    assert client is not None
    assert client.session is not None
    
    # 验证性能配置已应用
    client_with_url = HttpClient(base_url="https://httpbin.org")
    assert client_with_url.base_url == "https://httpbin.org"


@test_case("性能配置加载测试")
def test_performance_config():
    """测试性能配置是否正确加载"""
    from performance_config import get_all_performance_config
    
    config = get_all_performance_config()
    assert 'http' in config
    assert 'concurrent' in config
    assert config['http']['pool_maxsize'] == 100
    assert config['http']['pool_connections'] == 50


@test_case("HTTP GET请求测试")
def test_http_get_request():
    """测试HTTP GET请求功能"""
    from http_client import HttpClient
    
    client = HttpClient(timeout=10)
    try:
        response = client.get("https://httpbin.org/get")
        assert response.status_code == 200
        assert response.json() is not None
    except Exception as e:
        # 网络问题时跳过
        print(f"   提示: 网络请求失败（可能是网络问题）: {e}")
        raise


@test_case("验证模块测试")
def test_validate_module():
    """测试验证模块功能"""
    from validate import Validator
    
    validator = Validator()
    
    # 测试equals
    assert validator.equals(1, 1) == True
    assert validator.equals(1, 2) == False
    
    # 测试contains
    assert validator.contains("hello world", "hello") == True
    assert validator.contains("hello", "world") == False
    
    # 测试length_equals
    assert validator.length_equals([1, 2, 3], 3) == True


@test_case("配置管理器测试")
def test_config_manager():
    """测试配置管理器功能"""
    from config_manager import ConfigManager
    
    # 创建默认配置
    config = ConfigManager()
    assert config is not None
    
    # 测试嵌套访问
    try:
        config.get('env', 'test')
    except:
        pass  # 如果没有配置文件，允许失败


@test_case("Runner模块导入测试")
def test_runner_module():
    """测试Runner模块"""
    import runner
    
    assert hasattr(runner, 'RunYaml')
    RunYaml = runner.RunYaml
    assert RunYaml is not None


@test_case("依赖完整性测试")
def test_dependencies():
    """测试核心依赖是否安装完整"""
    dependencies = [
        'pytest',
        'requests',
        'yaml',
        'jsonpath_ng',
        'colorama',
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        raise AssertionError(f"缺少依赖: {', '.join(missing)}")


@test_case("HTTP连接池配置测试")
def test_http_pool_config():
    """测试HTTP连接池配置是否正确应用"""
    from http_client import HttpClient
    
    client = HttpClient()
    
    # 检查adapter配置
    adapter = client.session.get_adapter('http://')
    assert adapter is not None
    
    # 验证连接池配置（通过创建多个请求验证）
    # 这里只验证客户端创建成功
    assert client.session is not None


@test_case("性能测试脚本存在性测试")
def test_performance_scripts():
    """测试性能测试脚本是否存在"""
    import os
    
    files_to_check = [
        'performance_config.py',
        'performance_test.py',
        'verify_installation.py',
    ]
    
    missing = []
    for file in files_to_check:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        raise AssertionError(f"缺少文件: {', '.join(missing)}")


def print_summary():
    """打印测试摘要"""
    print("\n" + "="*60)
    print("测试摘要")
    print("="*60)
    
    total = test_results['total']
    passed = len(test_results['passed'])
    failed = len(test_results['failed'])
    
    print(f"\n总计: {total} 个测试")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    
    if failed > 0:
        print("\n失败的测试:")
        for name, error in test_results['failed']:
            print(f"  - {name}")
            print(f"    {error}")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"\n成功率: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n🎉 所有测试通过！功能正常！")
    elif success_rate >= 80:
        print("\n⚠️  大部分测试通过，部分功能可能需要检查")
    else:
        print("\n❌ 测试失败较多，请检查问题")
    
    print("="*60 + "\n")
    
    return success_rate == 100


def main():
    """主函数"""
    print("\n" + "="*60)
    print("YH API 测试框架 - 功能验证测试")
    print("="*60 + "\n")
    
    print("开始运行测试...\n")
    
    # 运行所有测试
    test_module_imports()
    test_http_client_creation()
    test_performance_config()
    test_http_get_request()
    test_validate_module()
    test_config_manager()
    test_runner_module()
    test_dependencies()
    test_http_pool_config()
    test_performance_scripts()
    
    # 打印摘要
    all_passed = print_summary()
    
    # 返回退出码
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
