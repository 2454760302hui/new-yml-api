"""
示例测试文件
演示如何编写测试用例
"""

import pytest


def test_example():
    """示例测试：基础断言"""
    assert 1 + 1 == 2


def test_string_operations():
    """示例测试：字符串操作"""
    text = "Hello, World!"
    assert text.startswith("Hello")
    assert "World" in text
    assert len(text) == 13


@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input_value, expected):
    """示例测试：参数化测试"""
    assert input_value * 2 == expected


class TestExample:
    """示例测试类"""
    
    def test_list_operations(self):
        """测试列表操作"""
        my_list = [1, 2, 3]
        my_list.append(4)
        assert len(my_list) == 4
        assert my_list[-1] == 4
    
    def test_dict_operations(self):
        """测试字典操作"""
        my_dict = {"name": "test", "value": 123}
        assert my_dict["name"] == "test"
        assert "value" in my_dict
