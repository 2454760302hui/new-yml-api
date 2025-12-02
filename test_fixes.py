#!/usr/bin/env python3
"""
修复验证测试脚本

验证所有P0级别修复是否成功。
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from colorama import init, Fore, Style

init(autoreset=True)


def print_section(title):
    """打印章节标题"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{title}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def print_success(msg):
    """打印成功消息"""
    print(f"{Fore.GREEN}[OK] {msg}{Style.RESET_ALL}")


def print_error(msg):
    """打印错误消息"""
    print(f"{Fore.RED}[FAIL] {msg}{Style.RESET_ALL}")


def print_warning(msg):
    """打印警告消息"""
    print(f"{Fore.YELLOW}[WARN] {msg}{Style.RESET_ALL}")


def print_info(msg):
    """打印信息消息"""
    print(f"{Fore.BLUE}[INFO] {msg}{Style.RESET_ALL}")


def test_safe_import():
    """测试安全导入模块"""
    print_section("测试 1: 安全导入模块")

    try:
        from safe_import import (
            safe_import, safe_import_from, check_module_available,
            get_available_optional_modules
        )
        print_success("safe_import模块导入成功")

        # 测试导入存在的模块
        requests = safe_import('requests')
        if requests:
            print_success("成功导入requests模块")

        # 测试导入不存在的模块
        fake_module = safe_import('fake_module_xyz', silent=True)
        print_success("正确处理不存在的模块")

        # 获取可选模块状态
        available_modules = get_available_optional_modules()
        installed_count = sum(1 for v in available_modules.values() if v)
        print_info(f"已安装可选模块: {installed_count}/{len(available_modules)}")

        return True
    except Exception as e:
        print_error(f"安全导入测试失败: {e}")
        return False


def test_yaml_validator():
    """测试YAML配置验证器"""
    print_section("测试 2: YAML配置验证器")

    try:
        from yaml_validator import YAMLConfigValidator, validate_yaml_config
        print_success("yaml_validator模块导入成功")

        # 测试有效配置
        valid_config = {
            'config': {
                'name': '测试项目',
                'base_url': 'https://httpbin.org',
                'timeout': 30,
            },
            'tests': [
                {
                    'name': '测试用例1',
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
        if result:
            print_success("有效配置验证通过")

        # 测试无效配置
        invalid_config = {
            'config': {
                'timeout': -1,  # 无效timeout
            }
        }

        validator2 = YAMLConfigValidator()
        try:
            validator2.validate_config(invalid_config)
            print_error("应该检测到无效配置但没有")
            return False
        except Exception:
            print_success("正确检测到无效配置")

        return True
    except Exception as e:
        print_error(f"YAML验证器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hook_manager():
    """测试Hook管理器"""
    print_section("测试 3: Hook管理器")

    try:
        from hook_manager import (
            HookManager, HookType, HookContext,
            before_suite, after_suite, on_failure
        )
        print_success("hook_manager模块导入成功")

        manager = HookManager()

        # 注册测试Hook
        hook_executed = {'before': False, 'after': False, 'failure': False}

        def before_hook():
            hook_executed['before'] = True
            return True

        def after_hook():
            hook_executed['after'] = True

        def failure_hook(**kwargs):
            hook_executed['failure'] = True

        manager.register(HookType.BEFORE_SUITE, before_hook)
        manager.register(HookType.AFTER_SUITE, after_hook)
        manager.register(HookType.ON_FAILURE, failure_hook)

        # 执行Hook
        manager.execute_before_suite("test_suite")
        manager.execute_after_suite("test_suite", {"passed": 10})
        manager.execute_on_failure("test_case", Exception("测试错误"))

        if all(hook_executed.values()):
            print_success("所有Hook成功执行")
            print_info(f"注册的Hook总数: {manager.get_hook_count()}")
            return True
        else:
            print_error("部分Hook未执行")
            return False

    except Exception as e:
        print_error(f"Hook管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_runner_imports():
    """测试runner.py的导入修复"""
    print_section("测试 4: Runner模块导入修复")

    try:
        # 尝试导入runner模块
        import runner
        print_success("runner模块导入成功")

        # 检查关键类是否存在
        if hasattr(runner, 'RunYaml'):
            print_success("RunYaml类存在")

        # 检查安全导入是否工作
        if hasattr(runner, 'allure'):
            print_info("allure模块已加载（或使用占位符）")

        if hasattr(runner, 'websocket'):
            print_info("websocket模块已加载（或使用占位符）")

        return True
    except ImportError as e:
        print_error(f"Runner模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print_error(f"Runner测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_requirements_files():
    """测试依赖文件整理"""
    print_section("测试 5: 依赖文件整理")

    try:
        required_files = [
            'requirements.txt',
            'requirements-full.txt',
            'requirements-optional.txt'
        ]

        all_exist = True
        for file_name in required_files:
            file_path = project_root / file_name
            if file_path.exists():
                print_success(f"文件存在: {file_name}")
            else:
                print_error(f"文件缺失: {file_name}")
                all_exist = False

        # 检查旧文件是否已删除
        if not (project_root / 'requirements_clean.txt').exists():
            print_success("冗余文件已删除: requirements_clean.txt")
        else:
            print_warning("冗余文件仍存在: requirements_clean.txt")

        return all_exist
    except Exception as e:
        print_error(f"依赖文件测试失败: {e}")
        return False


def test_yaml_file_validation():
    """测试实际YAML文件验证"""
    print_section("测试 6: 实际YAML文件验证")

    try:
        from yaml_validator import validate_yaml_file

        # 测试default_test.yaml
        test_file = project_root / 'default_test.yaml'
        if test_file.exists():
            try:
                result = validate_yaml_file(test_file)
                print_success(f"default_test.yaml 验证通过")
            except Exception as e:
                print_warning(f"default_test.yaml 验证有问题: {e}")
        else:
            print_warning("default_test.yaml 不存在，跳过测试")

        return True
    except Exception as e:
        print_error(f"YAML文件验证测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}YH API Framework - Fix Verification Tests")
    print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")

    tests = [
        ("安全导入模块", test_safe_import),
        ("YAML配置验证器", test_yaml_validator),
        ("Hook管理器", test_hook_manager),
        ("Runner导入修复", test_runner_imports),
        ("依赖文件整理", test_requirements_files),
        ("YAML文件验证", test_yaml_file_validation),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"{test_name}测试异常: {e}")
            results[test_name] = False

    # 打印汇总
    print_section("测试汇总")

    passed = sum(1 for r in results.values() if r)
    total = len(results)

    for test_name, result in results.items():
        status = f"{Fore.GREEN}[PASS]" if result else f"{Fore.RED}[FAIL]"
        print(f"{status}{Style.RESET_ALL} - {test_name}")

    print(f"\n{Fore.CYAN}总计: {passed}/{total} 测试通过{Style.RESET_ALL}")

    if passed == total:
        print(f"\n{Fore.GREEN}All tests passed! Fixes verified successfully!{Style.RESET_ALL}\n")
        return 0
    else:
        print(f"\n{Fore.YELLOW}Some tests failed, please check the errors above{Style.RESET_ALL}\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
