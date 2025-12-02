"""
安装验证脚本
Installation Verification Script

验证依赖安装是否正确
"""

import sys
import importlib
from typing import List, Tuple

# 定义颜色代码（如果 colorama 可用）
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = YELLOW = BLUE = RESET = ""


def check_module(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """
    检查模块是否可导入
    
    Args:
        module_name: 模块名称
        package_name: 包名称（用于提示安装）
        
    Returns:
        (是否成功, 版本信息)
    """
    if package_name is None:
        package_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'unknown')
        return True, version
    except ImportError:
        return False, package_name


def verify_core_dependencies():
    """验证核心依赖"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  核心依赖检查{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    core_modules = [
        ('pytest', 'pytest'),
        ('requests', 'requests'),
        ('yaml', 'PyYAML'),
        ('jsonpath_ng', 'jsonpath-ng'),
        ('colorama', 'colorama'),
    ]
    
    all_ok = True
    
    for module_name, package_name in core_modules:
        success, info = check_module(module_name, package_name)
        if success:
            print(f"{GREEN}✅ {package_name:20} v{info}{RESET}")
        else:
            print(f"{RED}❌ {package_name:20} 未安装{RESET}")
            all_ok = False
    
    return all_ok


def verify_optional_dependencies():
    """验证可选依赖"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  可选依赖检查{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    optional_modules = [
        ('allure', 'allure-pytest', 'reporting'),
        ('fastapi', 'fastapi', 'docs'),
        ('pymysql', 'pymysql', 'database'),
        ('redis', 'redis', 'database'),
        ('websockets', 'websockets', 'socket'),
        ('faker', 'faker', 'data'),
        ('pandas', 'pandas', 'data'),
    ]
    
    installed_count = 0
    
    for module_name, package_name, feature in optional_modules:
        success, info = check_module(module_name, package_name)
        if success:
            print(f"{GREEN}✅ {package_name:20} v{info:15} [{feature}]{RESET}")
            installed_count += 1
        else:
            print(f"{YELLOW}⚪ {package_name:20} 未安装          [{feature}]{RESET}")
    
    print(f"\n已安装可选依赖: {installed_count}/{len(optional_modules)}")
    
    if installed_count < len(optional_modules):
        print(f"\n{YELLOW}💡 安装提示:{RESET}")
        print(f"   pip install api-test-yh-pro[reporting]  # 报告功能")
        print(f"   pip install api-test-yh-pro[docs]       # 文档服务器")
        print(f"   pip install api-test-yh-pro[database]   # 数据库支持")
        print(f"   pip install api-test-yh-pro[full]       # 完整功能")


def check_performance_config():
    """检查性能配置"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  性能配置检查{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    try:
        from performance_config import get_all_performance_config
        config = get_all_performance_config()
        
        print(f"{GREEN}✅ 性能配置文件已加载{RESET}")
        print(f"\n核心配置:")
        print(f"  - HTTP连接池: {config['http']['pool_maxsize']}")
        print(f"  - 并发线程数: {config['concurrent']['max_workers']}")
        print(f"  - 重试次数: {config['http']['max_retries']}")
        
        return True
    except ImportError:
        print(f"{YELLOW}⚠️  性能配置文件未找到{RESET}")
        return False


def check_project_files():
    """检查项目文件"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  项目文件检查{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    import os
    
    required_files = [
        'runner.py',
        'http_client.py',
        'validate.py',
        'requirements.txt',
        'pyproject.toml',
    ]
    
    optional_files = [
        'performance_config.py',
        'config.py',
        'QUICKSTART.md',
        'IMPROVEMENTS.md',
    ]
    
    all_ok = True
    
    print("核心文件:")
    for file in required_files:
        if os.path.exists(file):
            print(f"{GREEN}✅ {file}{RESET}")
        else:
            print(f"{RED}❌ {file} 缺失{RESET}")
            all_ok = False
    
    print("\n新增文件:")
    for file in optional_files:
        if os.path.exists(file):
            print(f"{GREEN}✅ {file}{RESET}")
        else:
            print(f"{YELLOW}⚪ {file}{RESET}")
    
    return all_ok


def show_python_info():
    """显示Python环境信息"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  Python 环境信息{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")


def main():
    """主函数"""
    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}  YH API 测试框架 - 安装验证{RESET}")
    print(f"{GREEN}{'='*60}{RESET}")
    
    # Python环境
    show_python_info()
    
    # 核心依赖
    core_ok = verify_core_dependencies()
    
    # 可选依赖
    verify_optional_dependencies()
    
    # 性能配置
    perf_ok = check_performance_config()
    
    # 项目文件
    files_ok = check_project_files()
    
    # 总结
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}  验证总结{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    if core_ok and files_ok:
        print(f"{GREEN}✅ 核心功能正常，可以开始使用！{RESET}")
        print(f"\n{BLUE}快速开始:{RESET}")
        print(f"  1. 查看快速指南: cat QUICKSTART.md")
        print(f"  2. 运行示例测试: python runner.py tests/test_example.yaml")
        print(f"  3. 性能测试: python performance_test.py")
    else:
        print(f"{RED}❌ 发现问题，请检查上述错误{RESET}")
        if not core_ok:
            print(f"\n{YELLOW}💡 修复核心依赖:{RESET}")
            print(f"   pip install -r requirements.txt")
    
    if perf_ok:
        print(f"\n{GREEN}🚀 性能优化已启用{RESET}")
    
    print(f"\n{BLUE}{'='*60}{RESET}\n")


if __name__ == "__main__":
    main()
