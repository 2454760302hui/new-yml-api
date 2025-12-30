"""
增强的Hook系统

提供完整的测试生命周期Hook支持，包括套件级、用例级、失败处理等。
"""

from typing import Dict, Any, Callable, List, Optional
from enum import Enum
import inspect
from logging_config import get_logger

log = get_logger()


class HookType(Enum):
    """Hook类型枚举"""
    BEFORE_SUITE = "before_suite"       # 测试套件开始前
    AFTER_SUITE = "after_suite"         # 测试套件结束后
    BEFORE_MODULE = "before_module"     # 模块开始前
    AFTER_MODULE = "after_module"       # 模块结束后
    BEFORE_TEST = "before_test"         # 每个测试用例前
    AFTER_TEST = "after_test"           # 每个测试用例后
    BEFORE_REQUEST = "before_request"   # 每个请求前
    AFTER_REQUEST = "after_request"     # 每个请求后
    ON_SUCCESS = "on_success"           # 测试成功时
    ON_FAILURE = "on_failure"           # 测试失败时
    ON_ERROR = "on_error"               # 发生错误时
    ON_SKIP = "on_skip"                 # 测试跳过时
    TEARDOWN = "teardown"               # 清理操作


class HookContext:
    """Hook执行上下文"""

    def __init__(self):
        self.suite_name: Optional[str] = None
        self.module_name: Optional[str] = None
        self.test_name: Optional[str] = None
        self.request_data: Optional[Dict[str, Any]] = None
        self.response_data: Optional[Dict[str, Any]] = None
        self.error: Optional[Exception] = None
        self.result: Optional[Dict[str, Any]] = None
        self.variables: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}

    def update(self, **kwargs):
        """更新上下文"""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'suite_name': self.suite_name,
            'module_name': self.module_name,
            'test_name': self.test_name,
            'request_data': self.request_data,
            'response_data': self.response_data,
            'error': str(self.error) if self.error else None,
            'result': self.result,
            'variables': self.variables,
            'metadata': self.metadata,
        }


class HookManager:
    """Hook管理器"""

    def __init__(self):
        self.hooks: Dict[HookType, List[Callable]] = {
            hook_type: [] for hook_type in HookType
        }
        self.context = HookContext()
        self.enabled = True

    def register(self, hook_type: HookType, func: Callable, priority: int = 0):
        """
        注册Hook函数

        Args:
            hook_type: Hook类型
            func: Hook函数
            priority: 优先级（数字越小优先级越高）
        """
        if not callable(func):
            raise TypeError(f"Hook函数必须是可调用对象: {func}")

        self.hooks[hook_type].append((priority, func))
        # 按优先级排序
        self.hooks[hook_type].sort(key=lambda x: x[0])

        log.debug(f"注册Hook: {hook_type.value} -> {func.__name__} (优先级: {priority})")

    def register_from_config(self, hook_config: Dict[str, Any]):
        """
        从配置注册Hook

        Args:
            hook_config: Hook配置字典

        Examples:
            >>> config = {
            ...     'before_suite': 'setup_suite',
            ...     'after_suite': 'teardown_suite',
            ...     'on_failure': 'handle_failure'
            ... }
        """
        for hook_type_str, func_name in hook_config.items():
            try:
                hook_type = HookType(hook_type_str)
            except ValueError:
                log.warning(f"未知的Hook类型: {hook_type_str}")
                continue

            # 这里需要从全局命名空间或模块中查找函数
            # 实际实现时需要传入函数查找器
            log.debug(f"从配置注册Hook: {hook_type.value} -> {func_name}")

    def execute(self, hook_type: HookType, context: Optional[HookContext] = None,
                **kwargs) -> bool:
        """
        执行Hook

        Args:
            hook_type: Hook类型
            context: Hook上下文
            **kwargs: 传递给Hook函数的参数

        Returns:
            是否所有Hook都成功执行
        """
        if not self.enabled:
            log.debug(f"Hook系统已禁用，跳过执行: {hook_type.value}")
            return True

        if hook_type not in self.hooks or not self.hooks[hook_type]:
            log.debug(f"未注册Hook: {hook_type.value}")
            return True

        # 使用提供的上下文或默认上下文
        ctx = context or self.context
        ctx.update(**kwargs)

        log.debug(f"执行Hook: {hook_type.value} (共{len(self.hooks[hook_type])}个)")

        all_success = True
        for priority, func in self.hooks[hook_type]:
            try:
                # 检查函数签名
                sig = inspect.signature(func)
                if 'context' in sig.parameters:
                    result = func(context=ctx)
                elif len(sig.parameters) == 0:
                    result = func()
                else:
                    result = func(**kwargs)

                # 如果Hook返回False，中断执行
                if result is False:
                    log.warning(f"Hook返回False，中断执行: {func.__name__}")
                    all_success = False
                    break

            except Exception as e:
                log.error(f"Hook执行失败: {func.__name__}, 错误: {e}")
                all_success = False

                # 如果是on_error hook本身失败，不要递归调用
                if hook_type != HookType.ON_ERROR:
                    self.execute(HookType.ON_ERROR, context=ctx, error=e)

        return all_success

    def execute_before_suite(self, suite_name: str, **kwargs):
        """执行套件前Hook"""
        self.context.suite_name = suite_name
        return self.execute(HookType.BEFORE_SUITE, suite_name=suite_name, **kwargs)

    def execute_after_suite(self, suite_name: str, result: Dict[str, Any], **kwargs):
        """执行套件后Hook"""
        return self.execute(HookType.AFTER_SUITE, suite_name=suite_name,
                          result=result, **kwargs)

    def execute_before_test(self, test_name: str, **kwargs):
        """执行测试用例前Hook"""
        self.context.test_name = test_name
        return self.execute(HookType.BEFORE_TEST, test_name=test_name, **kwargs)

    def execute_after_test(self, test_name: str, result: Dict[str, Any], **kwargs):
        """执行测试用例后Hook"""
        return self.execute(HookType.AFTER_TEST, test_name=test_name,
                          result=result, **kwargs)

    def execute_before_request(self, request_data: Dict[str, Any], **kwargs):
        """执行请求前Hook"""
        self.context.request_data = request_data
        return self.execute(HookType.BEFORE_REQUEST, request_data=request_data,
                          **kwargs)

    def execute_after_request(self, request_data: Dict[str, Any],
                            response_data: Dict[str, Any], **kwargs):
        """执行请求后Hook"""
        self.context.response_data = response_data
        return self.execute(HookType.AFTER_REQUEST, request_data=request_data,
                          response_data=response_data, **kwargs)

    def execute_on_success(self, test_name: str, result: Dict[str, Any], **kwargs):
        """执行成功Hook"""
        return self.execute(HookType.ON_SUCCESS, test_name=test_name,
                          result=result, **kwargs)

    def execute_on_failure(self, test_name: str, error: Exception, **kwargs):
        """执行失败Hook"""
        self.context.error = error
        return self.execute(HookType.ON_FAILURE, test_name=test_name,
                          error=error, **kwargs)

    def execute_on_error(self, error: Exception, **kwargs):
        """执行错误Hook"""
        self.context.error = error
        return self.execute(HookType.ON_ERROR, error=error, **kwargs)

    def execute_teardown(self, **kwargs):
        """执行清理Hook"""
        return self.execute(HookType.TEARDOWN, **kwargs)

    def clear_hooks(self, hook_type: Optional[HookType] = None):
        """
        清除Hook

        Args:
            hook_type: Hook类型，如果为None则清除所有Hook
        """
        if hook_type:
            self.hooks[hook_type] = []
            log.debug(f"清除Hook: {hook_type.value}")
        else:
            self.hooks = {hook_type: [] for hook_type in HookType}
            log.debug("清除所有Hook")

    def enable(self):
        """启用Hook系统"""
        self.enabled = True
        log.debug("Hook系统已启用")

    def disable(self):
        """禁用Hook系统"""
        self.enabled = False
        log.debug("Hook系统已禁用")

    def get_hook_count(self, hook_type: Optional[HookType] = None) -> int:
        """
        获取Hook数量

        Args:
            hook_type: Hook类型，如果为None则返回总数

        Returns:
            Hook数量
        """
        if hook_type:
            return len(self.hooks[hook_type])
        else:
            return sum(len(hooks) for hooks in self.hooks.values())


# 全局Hook管理器实例
_global_hook_manager = None


def get_hook_manager() -> HookManager:
    """获取全局Hook管理器"""
    global _global_hook_manager
    if _global_hook_manager is None:
        _global_hook_manager = HookManager()
    return _global_hook_manager


# 便捷装饰器
def before_suite(func: Callable) -> Callable:
    """before_suite装饰器"""
    get_hook_manager().register(HookType.BEFORE_SUITE, func)
    return func


def after_suite(func: Callable) -> Callable:
    """after_suite装饰器"""
    get_hook_manager().register(HookType.AFTER_SUITE, func)
    return func


def before_test(func: Callable) -> Callable:
    """before_test装饰器"""
    get_hook_manager().register(HookType.BEFORE_TEST, func)
    return func


def after_test(func: Callable) -> Callable:
    """after_test装饰器"""
    get_hook_manager().register(HookType.AFTER_TEST, func)
    return func


def on_failure(func: Callable) -> Callable:
    """on_failure装饰器"""
    get_hook_manager().register(HookType.ON_FAILURE, func)
    return func


if __name__ == '__main__':
    # 测试Hook系统
    print("测试Hook系统...")

    manager = HookManager()

    # 注册Hook
    @before_suite
    def setup():
        print("执行setup")
        return True

    @after_suite
    def cleanup():
        print("执行cleanup")

    @on_failure
    def handle_failure(error):
        print(f"处理失败: {error}")

    # 执行Hook
    manager.execute_before_suite("test_suite")
    manager.execute_after_suite("test_suite", {"passed": 10, "failed": 2})
    manager.execute_on_failure("test_case_1", Exception("测试失败"))

    print(f"✅ Hook总数: {manager.get_hook_count()}")
