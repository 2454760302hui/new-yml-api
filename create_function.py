"""
动态函数创建模块
用于从参数动态创建测试函数
"""

from inspect import Parameter, Signature
from typing import Callable, List, Any
import types


def create_function_from_parameters(
    func: Callable,
    parameters: List[Parameter],
    documentation: str = "",
    func_name: str = None,
    func_filename: str = None
) -> Callable:
    """
    从参数列表动态创建函数
    
    Args:
        func: 原始函数
        parameters: 参数列表
        documentation: 函数文档
        func_name: 函数名称
        func_filename: 函数所在文件名
    
    Returns:
        动态创建的函数
    """
    # 创建新的函数签名
    sig = Signature(parameters=parameters)
    
    # 创建新函数
    new_func = types.FunctionType(
        func.__code__,
        func.__globals__,
        name=func_name or func.__name__,
        argdefs=func.__defaults__,
        closure=func.__closure__
    )
    
    # 设置函数签名
    new_func.__signature__ = sig
    
    # 设置函数文档
    if documentation:
        new_func.__doc__ = documentation
    
    # 设置函数所属文件
    if func_filename:
        new_func.__code__ = new_func.__code__.replace(
            co_filename=func_filename
        )
    
    return new_func
