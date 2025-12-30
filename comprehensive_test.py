#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面功能自测脚本

测试所有修复的功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("YH API Framework - Comprehensive Functional Test")
print("=" * 70)
print()

# 测试结果收集
test_results = {}


def test_module(name, test_func):
    """运行单个测试模块"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    try:
        result = test_func()
        test_results[name] = result
        status = "[PASS]" if result else "[FAIL]"
        print(f"\n{status} {name}")
        return result
    except Exception as e:
        print(f"\n[ERROR] {name}: {e}")
        import traceback
        traceback.print_exc()
        test_results[name] = False
        return False


# ============================================================
# 测试1: 安全导入模块功能测试
# ============================================================
def test_safe_import_module():
    """测试安全导入模块的所有功能"""
    print("\n1. Testing safe_import module...")

    from safe_import import (
        safe_import, safe_import_from, check_module_available,
        get_available_optional_modules, OptionalModule
    )

    # 测试1.1: 导入存在的模块
    print("\n1.1 Import existing module (requests)...")
    requests = safe_import('requests')
    assert requests is not None
    print("  [OK] requests module imported successfully")

    # 测试1.2: 导入不存在的模块
    print("\n1.2 Import non-existing module...")
    fake_module = safe_import('fake_module_xyz_123', silent=True)
    assert isinstance(fake_module, OptionalModule)
    print("  [OK] Non-existing module handled correctly")

    # 测试1.3: 尝试使用不存在模块的功能
    print("\n1.3 Try to use non-existing module...")
    try:
        fake_module.some_function()
        print("  [FAIL] Should have raised ImportError")
        return False
    except ImportError as e:
        print(f"  [OK] Correctly raised ImportError: {str(e)[:50]}...")

    # 测试1.4: safe_import_from
    print("\n1.4 Testing safe_import_from...")
    result = safe_import_from('requests', 'get', 'post', silent=False)
    assert len(result) == 2
    print("  [OK] safe_import_from works correctly")

    # 测试1.5: check_module_available
    print("\n1.5 Testing check_module_available...")
    assert check_module_available('requests') == True
    assert check_module_available('fake_xyz_123') == False
    print("  [OK] check_module_available works correctly")

    # 测试1.6: get_available_optional_modules
    print("\n1.6 Testing get_available_optional_modules...")
    available = get_available_optional_modules()
    assert isinstance(available, dict)
    installed = sum(1 for v in available.values() if v)
    print(f"  [OK] Found {installed}/{len(available)} optional modules installed")

    return True


# ============================================================
# 测试2: YAML配置验证器功能测试
# ============================================================
def test_yaml_validator_module():
    """测试YAML配置验证器的所有功能"""
    print("\n2. Testing yaml_validator module...")

    from yaml_validator import YAMLConfigValidator, validate_yaml_config
    import exceptions

    # 测试2.1: 验证有效配置
    print("\n2.1 Validate valid configuration...")
    valid_config = {
        'config': {
            'name': 'Test Project',
            'base_url': 'https://httpbin.org',
            'timeout': 30,
            'retry_count': 3,
        },
        'tests': [
            {
                'name': 'Test Case 1',
                'request': {
                    'method': 'GET',
                    'url': '/get',
                },
                'validate': [
                    {'check': 'status_code', 'expected': 200}
                ]
            }
        ]
    }

    validator = YAMLConfigValidator()
    result = validator.validate_config(valid_config)
    assert result == True
    print("  [OK] Valid configuration passed validation")

    # 测试2.2: 检测无效timeout
    print("\n2.2 Detect invalid timeout...")
    invalid_config1 = {
        'config': {
            'timeout': -1,  # 无效
        }
    }

    validator2 = YAMLConfigValidator()
    try:
        validator2.validate_config(invalid_config1)
        print("  [FAIL] Should have detected invalid timeout")
        return False
    except exceptions.ConfigError:
        print("  [OK] Invalid timeout detected correctly")

    # 测试2.3: 检测无效HTTP方法
    print("\n2.3 Detect invalid HTTP method...")
    invalid_config2 = {
        'config': {},
        'tests': [
            {
                'request': {
                    'method': 'INVALID_METHOD',
                    'url': '/test'
                }
            }
        ]
    }

    validator3 = YAMLConfigValidator()
    try:
        validator3.validate_config(invalid_config2)
        print("  [FAIL] Should have detected invalid HTTP method")
        return False
    except exceptions.ConfigError:
        print("  [OK] Invalid HTTP method detected correctly")

    # 测试2.4: 验证报告功能
    print("\n2.4 Test validation report...")
    report = validator3.get_validation_report()
    assert 'errors' in report
    assert 'warnings' in report
    assert report['error_count'] > 0
    print(f"  [OK] Validation report generated (errors: {report['error_count']})")

    # 测试2.5: 验证实际YAML文件
    print("\n2.5 Validate actual YAML file...")
    test_file = project_root / 'default_test.yaml'
    if test_file.exists():
        from yaml_validator import validate_yaml_file
        try:
            validate_yaml_file(test_file)
            print("  [OK] default_test.yaml validation passed")
        except Exception as e:
            print(f"  [WARN] default_test.yaml validation issue: {e}")
    else:
        print("  [SKIP] default_test.yaml not found")

    return True


# ============================================================
# 测试3: Hook管理器功能测试
# ============================================================
def test_hook_manager_module():
    """测试Hook管理器的所有功能"""
    print("\n3. Testing hook_manager module...")

    from hook_manager import (
        HookManager, HookType, HookContext,
        get_hook_manager, before_suite, after_suite
    )

    # 测试3.1: 创建Hook管理器
    print("\n3.1 Create hook manager...")
    manager = HookManager()
    assert manager is not None
    print("  [OK] Hook manager created")

    # 测试3.2: 注册Hook
    print("\n3.2 Register hooks...")
    hook_calls = {'before': 0, 'after': 0, 'failure': 0}

    def before_hook():
        hook_calls['before'] += 1
        return True

    def after_hook(**kwargs):
        hook_calls['after'] += 1

    def failure_hook(**kwargs):
        hook_calls['failure'] += 1

    manager.register(HookType.BEFORE_SUITE, before_hook, priority=0)
    manager.register(HookType.AFTER_SUITE, after_hook, priority=0)
    manager.register(HookType.ON_FAILURE, failure_hook, priority=0)

    count = manager.get_hook_count()
    assert count == 3
    print(f"  [OK] {count} hooks registered")

    # 测试3.3: 执行Hook
    print("\n3.3 Execute hooks...")
    manager.execute_before_suite("test_suite")
    manager.execute_after_suite("test_suite", {"passed": 10})
    manager.execute_on_failure("test_case", Exception("Test error"))

    assert hook_calls['before'] == 1
    assert hook_calls['after'] == 1
    assert hook_calls['failure'] == 1
    print("  [OK] All hooks executed successfully")

    # 测试3.4: Hook优先级
    print("\n3.4 Test hook priority...")
    execution_order = []

    def hook_high():
        execution_order.append('high')
        return True

    def hook_low():
        execution_order.append('low')
        return True

    manager.register(HookType.BEFORE_TEST, hook_low, priority=10)
    manager.register(HookType.BEFORE_TEST, hook_high, priority=1)

    manager.execute_before_test("test")
    assert execution_order == ['high', 'low']
    print("  [OK] Hook priority works correctly")

    # 测试3.5: Hook启用/禁用
    print("\n3.5 Test hook enable/disable...")
    manager.disable()
    hook_calls['before'] = 0
    manager.execute_before_suite("test")
    assert hook_calls['before'] == 0
    print("  [OK] Hook disable works")

    manager.enable()
    manager.execute_before_suite("test")
    assert hook_calls['before'] == 1
    print("  [OK] Hook enable works")

    # 测试3.6: 清除Hook
    print("\n3.6 Test clear hooks...")
    manager.clear_hooks(HookType.BEFORE_TEST)
    count_before_test = len(manager.hooks[HookType.BEFORE_TEST])
    assert count_before_test == 0
    print("  [OK] Hook clearing works")

    return True


# ============================================================
# 测试4: Runner模块集成测试
# ============================================================
def test_runner_integration():
    """测试Runner模块的集成"""
    print("\n4. Testing runner module integration...")

    # 测试4.1: 导入runner模块
    print("\n4.1 Import runner module...")
    try:
        import runner
        print("  [OK] Runner module imported successfully")
    except ImportError as e:
        print(f"  [FAIL] Runner import failed: {e}")
        return False

    # 测试4.2: 检查RunYaml类
    print("\n4.2 Check RunYaml class...")
    assert hasattr(runner, 'RunYaml')
    print("  [OK] RunYaml class exists")

    # 测试4.3: 检查可选模块
    print("\n4.3 Check optional modules...")
    assert hasattr(runner, 'allure')
    assert hasattr(runner, 'websocket')
    print("  [OK] Optional modules loaded (or placeholders)")

    # 测试4.4: 检查配置验证集成
    print("\n4.4 Check config validation integration...")
    import types
    import yaml

    # 创建简单的测试配置
    test_config = {
        'config': {
            'base_url': 'https://httpbin.org',
        },
        'tests': [
            {
                'name': 'Simple Test',
                'request': {
                    'method': 'GET',
                    'url': '/get',
                }
            }
        ]
    }

    module = types.ModuleType('test_module')

    # 测试验证开启（默认）
    try:
        run_yaml = runner.RunYaml(test_config, module, {}, validate_config=True)
        print("  [OK] RunYaml with validation created")
    except Exception as e:
        print(f"  [FAIL] RunYaml creation failed: {e}")
        return False

    # 测试验证关闭
    try:
        run_yaml_no_val = runner.RunYaml(test_config, module, {}, validate_config=False)
        print("  [OK] RunYaml without validation created")
    except Exception as e:
        print(f"  [FAIL] RunYaml (no validation) creation failed: {e}")
        return False

    return True


# ============================================================
# 测试5: 依赖文件验证
# ============================================================
def test_requirements_files():
    """测试依赖文件的完整性"""
    print("\n5. Testing requirements files...")

    required_files = [
        'requirements.txt',
        'requirements-full.txt',
        'requirements-optional.txt',
    ]

    # 测试5.1: 检查文件存在
    print("\n5.1 Check files exist...")
    all_exist = True
    for filename in required_files:
        filepath = project_root / filename
        if filepath.exists():
            print(f"  [OK] {filename} exists")
        else:
            print(f"  [FAIL] {filename} missing")
            all_exist = False

    if not all_exist:
        return False

    # 测试5.2: 检查旧文件已删除
    print("\n5.2 Check redundant files removed...")
    old_file = project_root / 'requirements_clean.txt'
    if not old_file.exists():
        print("  [OK] requirements_clean.txt removed")
    else:
        print("  [WARN] requirements_clean.txt still exists")

    # 测试5.3: 验证文件内容
    print("\n5.3 Validate file contents...")

    # 检查requirements.txt
    with open(project_root / 'requirements.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'pytest>=' in content
        assert 'requests>=' in content
        assert 'PyYAML>=' in content
        print("  [OK] requirements.txt has core dependencies")

    # 检查requirements-full.txt
    with open(project_root / 'requirements-full.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        assert '-r requirements.txt' in content
        assert '-r requirements-optional.txt' in content
        print("  [OK] requirements-full.txt structure correct")

    return True


# ============================================================
# 测试6: 实际YAML文件执行测试（集成测试）
# ============================================================
def test_yaml_execution():
    """测试实际执行YAML配置文件"""
    print("\n6. Testing actual YAML execution...")

    # 创建一个简单的测试YAML配置
    print("\n6.1 Create test configuration...")
    test_yaml_content = """
config:
  name: "Integration Test"
  base_url: "https://httpbin.org"
  timeout: 10

tests:
  - name: "Simple GET Test"
    request:
      method: GET
      url: "/get"
      params:
        test: "integration"
    validate:
      - check: status_code
        expected: 200
"""

    import yaml
    import types

    config = yaml.safe_load(test_yaml_content)
    print("  [OK] Test configuration loaded")

    # 验证配置
    print("\n6.2 Validate configuration...")
    from yaml_validator import YAMLConfigValidator
    validator = YAMLConfigValidator()
    try:
        validator.validate_config(config)
        print("  [OK] Configuration validation passed")
    except Exception as e:
        print(f"  [FAIL] Configuration validation failed: {e}")
        return False

    # 创建RunYaml实例
    print("\n6.3 Create RunYaml instance...")
    import runner
    module = types.ModuleType('integration_test')

    try:
        run_yaml = runner.RunYaml(config, module, {})
        print("  [OK] RunYaml instance created")
    except Exception as e:
        print(f"  [FAIL] RunYaml creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 注意：我们不实际运行测试以避免网络依赖
    print("  [SKIP] Actual test execution (requires network)")

    return True


# ============================================================
# 主测试流程
# ============================================================
def main():
    """运行所有测试"""
    print("\nStarting comprehensive functional tests...\n")

    tests = [
        ("Safe Import Module", test_safe_import_module),
        ("YAML Validator Module", test_yaml_validator_module),
        ("Hook Manager Module", test_hook_manager_module),
        ("Runner Integration", test_runner_integration),
        ("Requirements Files", test_requirements_files),
        ("YAML Execution", test_yaml_execution),
    ]

    for test_name, test_func in tests:
        test_module(test_name, test_func)

    # 打印汇总
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in test_results.values() if r)
    total = len(test_results)

    for test_name, result in test_results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 70)

    if passed == total:
        print("\n[SUCCESS] All functional tests passed!")
        return 0
    else:
        print("\n[FAILED] Some tests failed. Please check the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
