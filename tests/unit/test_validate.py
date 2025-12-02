"""
验证模块单元测试
Unit Tests for Validation Module
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import validate


class TestEqualsValidation:
    """测试相等性验证"""
    
    def test_equals_integers(self):
        """测试整数相等"""
        validate.equals(1, 1)
        validate.equals(0, 0)
        validate.equals(-1, -1)
    
    def test_equals_strings(self):
        """测试字符串相等"""
        validate.equals("test", "test")
        validate.equals("", "")
    
    def test_equals_none(self):
        """测试None值相等"""
        validate.equals(None, None)
        validate.equals('None', None)
    
    def test_equals_fails(self):
        """测试不相等情况"""
        with pytest.raises(AssertionError):
            validate.equals(1, 2)


class TestComparisonValidation:
    """测试比较验证"""
    
    def test_less_than(self):
        """测试小于"""
        validate.less_than(1, 2)
        validate.less_than(0, 1)
        validate.less_than(-2, -1)
    
    def test_less_than_fails(self):
        """测试小于失败情况"""
        with pytest.raises(AssertionError):
            validate.less_than(2, 1)
        with pytest.raises(AssertionError):
            validate.less_than(1, 1)
    
    def test_less_than_or_equals(self):
        """测试小于等于"""
        validate.less_than_or_equals(1, 2)
        validate.less_than_or_equals(1, 1)
    
    def test_greater_than(self):
        """测试大于"""
        validate.greater_than(2, 1)
        validate.greater_than(1, 0)
    
    def test_greater_than_or_equals(self):
        """测试大于等于"""
        validate.greater_than_or_equals(2, 1)
        validate.greater_than_or_equals(1, 1)


class TestStringValidation:
    """测试字符串验证"""
    
    def test_string_equals(self):
        """测试字符串相等"""
        validate.string_equals("123", "123")
        validate.string_equals(123, "123")
    
    def test_startswith(self):
        """测试字符串开头"""
        validate.startswith("hello world", "hello")
        validate.startswith("test", "t")
    
    def test_startswith_fails(self):
        """测试字符串开头失败"""
        with pytest.raises(AssertionError):
            validate.startswith("hello", "world")
    
    def test_endswith(self):
        """测试字符串结尾"""
        validate.endswith("hello world", "world")
        validate.endswith("test", "t")
    
    def test_endswith_fails(self):
        """测试字符串结尾失败"""
        with pytest.raises(AssertionError):
            validate.endswith("hello", "world")


class TestLengthValidation:
    """测试长度验证"""
    
    def test_length_equals(self):
        """测试长度相等"""
        validate.length_equals("test", 4)
        validate.length_equals([1, 2, 3], 3)
        validate.length_equals({"a": 1, "b": 2}, 2)
    
    def test_length_equals_fails(self):
        """测试长度相等失败"""
        with pytest.raises(AssertionError):
            validate.length_equals("test", 5)
    
    def test_length_greater_than(self):
        """测试长度大于"""
        validate.length_greater_than("test", 3)
        validate.length_greater_than([1, 2, 3], 2)
    
    def test_length_less_than(self):
        """测试长度小于"""
        validate.length_less_than("test", 5)
        validate.length_less_than([1, 2], 3)


class TestContainsValidation:
    """测试包含验证"""
    
    def test_contains_in_string(self):
        """测试字符串包含"""
        validate.contains("hello world", "hello")
        validate.contains("test", "es")
    
    def test_contains_in_list(self):
        """测试列表包含"""
        validate.contains([1, 2, 3], 2)
        validate.contains(["a", "b", "c"], "b")
    
    def test_contains_in_dict(self):
        """测试字典包含"""
        validate.contains({"a": 1, "b": 2}, "a")
    
    def test_contains_fails(self):
        """测试包含失败"""
        with pytest.raises(AssertionError):
            validate.contains("hello", "world")


class TestRegexValidation:
    """测试正则验证"""
    
    def test_regex_match(self):
        """测试正则匹配"""
        validate.regex_match("test123", r"test\d+")
        validate.regex_match("abc", r"[a-z]+")
    
    def test_regex_match_fails(self):
        """测试正则匹配失败"""
        with pytest.raises(AssertionError):
            validate.regex_match("test", r"\d+")


class TestBoolValidation:
    """测试布尔验证"""
    
    def test_bool_equals_true(self):
        """测试布尔值为真"""
        validate.bool_equals(True, True)
        validate.bool_equals(1, True)
        validate.bool_equals("non-empty", True)
    
    def test_bool_equals_false(self):
        """测试布尔值为假"""
        validate.bool_equals(False, False)
        validate.bool_equals(0, False)
        validate.bool_equals("", False)
    
    def test_bool_equals_fails(self):
        """测试布尔验证失败"""
        with pytest.raises(AssertionError):
            validate.bool_equals(True, False)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
