"""
安全导入工具模块

提供安全的模块导入功能，处理可选依赖的导入问题。
"""

import importlib
import sys
from typing import Optional, Any
from logging_config import get_logger

log = get_logger()


class OptionalModule:
    """可选模块占位符"""

    def __init__(self, module_name: str):
        self.module_name = module_name
        self._warned = False

    def __getattr__(self, name):
        """访问模块属性时提示未安装"""
        if not self._warned:
            log.warning(
                f"模块 '{self.module_name}' 未安装，某些功能将不可用。"
                f"安装方式: pip install {self.module_name}"
            )
            self._warned = True

        # 返回一个空函数，避免AttributeError
        def _placeholder(*args, **kwargs):
            raise ImportError(
                f"'{self.module_name}' 模块未安装，无法使用 {name} 功能。"
                f"请安装: pip install {self.module_name}"
            )
        return _placeholder

    def __call__(self, *args, **kwargs):
        """模块被调用时提示"""
        raise ImportError(
            f"'{self.module_name}' 模块未安装。"
            f"请安装: pip install {self.module_name}"
        )


def safe_import(module_name: str,
                package: Optional[str] = None,
                silent: bool = False) -> Any:
    """
    安全导入模块，处理可选依赖

    Args:
        module_name: 模块名称
        package: 包名称（用于相对导入）
        silent: 是否静默模式（不记录警告）

    Returns:
        导入的模块对象，如果失败返回OptionalModule占位符

    Examples:
        >>> allure = safe_import('allure')
        >>> websocket = safe_import('websocket')
    """
    try:
        return importlib.import_module(module_name, package=package)
    except ImportError as e:
        if not silent:
            log.debug(f"可选模块 '{module_name}' 未安装: {e}")
        return OptionalModule(module_name)
    except Exception as e:
        log.error(f"导入模块 '{module_name}' 时发生错误: {e}")
        return OptionalModule(module_name)


def safe_import_from(module_name: str,
                     *names: str,
                     silent: bool = False) -> tuple:
    """
    从模块安全导入指定名称

    Args:
        module_name: 模块名称
        *names: 要导入的名称列表
        silent: 是否静默模式

    Returns:
        导入的对象元组

    Examples:
        >>> create_connection, WebSocket = safe_import_from('websocket', 'create_connection', 'WebSocket')
    """
    try:
        module = importlib.import_module(module_name)
        return tuple(getattr(module, name) for name in names)
    except ImportError as e:
        if not silent:
            log.debug(f"可选模块 '{module_name}' 未安装: {e}")
        placeholder = OptionalModule(module_name)
        return tuple(placeholder for _ in names)
    except AttributeError as e:
        log.error(f"模块 '{module_name}' 中未找到指定的属性: {e}")
        placeholder = OptionalModule(module_name)
        return tuple(placeholder for _ in names)
    except Exception as e:
        log.error(f"从模块 '{module_name}' 导入时发生错误: {e}")
        placeholder = OptionalModule(module_name)
        return tuple(placeholder for _ in names)


def check_module_available(module_name: str) -> bool:
    """
    检查模块是否可用

    Args:
        module_name: 模块名称

    Returns:
        模块是否可用
    """
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


def get_available_optional_modules() -> dict:
    """
    获取所有可选模块的可用状态

    Returns:
        模块名称到可用状态的字典
    """
    optional_modules = [
        'allure',
        'allure_pytest',
        'websocket',
        'pymysql',
        'redis',
        'pymongo',
        'sqlalchemy',
        'faker',
        'pandas',
        'openpyxl',
        'paramiko',
        'fastapi',
        'uvicorn',
        'pydantic',
    ]

    return {
        module: check_module_available(module)
        for module in optional_modules
    }


def log_available_modules():
    """记录可用的可选模块"""
    available = get_available_optional_modules()
    installed = [name for name, status in available.items() if status]
    missing = [name for name, status in available.items() if not status]

    if installed:
        log.debug(f"已安装的可选模块: {', '.join(installed)}")
    if missing:
        log.debug(f"未安装的可选模块: {', '.join(missing)}")


# 常用可选模块的预定义导入
def import_allure():
    """导入allure模块"""
    return safe_import('allure')


def import_websocket():
    """导入websocket模块"""
    return safe_import('websocket')


def import_database_modules():
    """导入数据库相关模块"""
    return {
        'pymysql': safe_import('pymysql'),
        'redis': safe_import('redis'),
        'pymongo': safe_import('pymongo'),
        'sqlalchemy': safe_import('sqlalchemy'),
    }


def import_data_modules():
    """导入数据处理模块"""
    return {
        'faker': safe_import('faker'),
        'pandas': safe_import('pandas'),
        'openpyxl': safe_import('openpyxl'),
    }


if __name__ == '__main__':
    # 测试安全导入
    print("测试安全导入功能...")

    # 测试导入存在的模块
    requests = safe_import('requests')
    print(f"requests模块: {requests}")

    # 测试导入不存在的模块
    fake_module = safe_import('fake_module_that_does_not_exist')
    print(f"fake_module: {fake_module}")

    # 测试调用不存在模块的方法
    try:
        fake_module.some_function()
    except ImportError as e:
        print(f"预期的错误: {e}")

    # 显示可用模块
    log_available_modules()
