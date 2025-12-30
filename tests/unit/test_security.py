#!/usr/bin/env python3
"""
单元测试 - runner.py 安全功能测试
测试安全条件评估和函数调用功能
"""

import pytest
from unittest.mock import Mock, patch
import types


# 我们需要模拟必要的模块
class MockModule:
    """模拟模块"""
    def __init__(self):
        self.__dict__ = {
            'len': len,
            'str': str,
            'int': int,
            'bool': bool,
            'print': print,
        }


class MockBuiltins:
    """模拟my_builtins模块"""
    __dict__ = {
        'len': len,
        'str': str,
        'int': int,
        'bool': bool,
        'print': print,
        'current_time': lambda: '2023-01-01',
    }


class TestSafeEvalCondition:
    """测试安全条件评估功能"""

    @pytest.fixture
    def run_yaml_instance(self):
        """创建RunYaml实例用于测试"""
        # 延迟导入避免循环依赖
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

        from runner import RunYaml

        raw = {'config': {'name': 'test'}}
        module = types.ModuleType('test_module')
        g = {}

        return RunYaml(raw, module, g, validate_config=False)

    def test_boolean_true(self, run_yaml_instance):
        """测试布尔值True"""
        assert run_yaml_instance._safe_eval_condition(True) is True

    def test_boolean_false(self, run_yaml_instance):
        """测试布尔值False"""
        assert run_yaml_instance._safe_eval_condition(False) is False

    def test_integer_zero(self, run_yaml_instance):
        """测试整数0"""
        assert run_yaml_instance._safe_eval_condition(0) is False

    def test_integer_positive(self, run_yaml_instance):
        """测试正整数"""
        assert run_yaml_instance._safe_eval_condition(1) is True
        assert run_yaml_instance._safe_eval_condition(42) is True

    def test_integer_negative(self, run_yaml_instance):
        """测试负整数"""
        assert run_yaml_instance._safe_eval_condition(-1) is True

    def test_float_zero(self, run_yaml_instance):
        """测试浮点数0.0"""
        assert run_yaml_instance._safe_eval_condition(0.0) is False

    def test_string_true_variants(self, run_yaml_instance):
        """测试字符串形式的True"""
        assert run_yaml_instance._safe_eval_condition("true") is True
        assert run_yaml_instance._safe_eval_condition("True") is True
        assert run_yaml_instance._safe_eval_condition("yes") is True
        assert run_yaml_instance._safe_eval_condition("1") is True

    def test_string_false_variants(self, run_yaml_instance):
        """测试字符串形式的False"""
        assert run_yaml_instance._safe_eval_condition("false") is False
        assert run_yaml_instance._safe_eval_condition("False") is False
        assert run_yaml_instance._safe_eval_condition("no") is False
        assert run_yaml_instance._safe_eval_condition("0") is False
        assert run_yaml_instance._safe_eval_condition("") is False

    def test_string_literal_eval(self, run_yaml_instance):
        """测试ast.literal_eval解析"""
        assert run_yaml_instance._safe_eval_condition("123") is True
        assert run_yaml_instance._safe_eval_condition("0") is False
        assert run_yaml_instance._safe_eval_condition("[1, 2, 3]") is True
        assert run_yaml_instance._safe_eval_condition("[]") is False

    def test_safe_comparison_expressions(self, run_yaml_instance):
        """测试安全的比较表达式"""
        # 设置context变量
        run_yaml_instance.context['x'] = 5
        run_yaml_instance.context['y'] = 10

        # 这些应该是安全的
        result = run_yaml_instance._safe_eval_condition("x > 3")
        assert result is True

        result = run_yaml_instance._safe_eval_condition("x < y")
        assert result is True

    def test_dangerous_import_pattern(self, run_yaml_instance):
        """测试检测危险的import模式"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的条件表达式"):
            run_yaml_instance._safe_eval_condition("import os")

        with pytest.raises(ParserError, match="不安全的条件表达式"):
            run_yaml_instance._safe_eval_condition("__import__('os')")

    def test_dangerous_exec_pattern(self, run_yaml_instance):
        """测试检测危险的exec模式"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的条件表达式"):
            run_yaml_instance._safe_eval_condition("exec('print(1)')")

    def test_dangerous_double_underscore(self, run_yaml_instance):
        """测试检测危险的__模式"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的条件表达式"):
            run_yaml_instance._safe_eval_condition("__class__")

    def test_dangerous_os_access(self, run_yaml_instance):
        """测试检测危险的os.模式"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的条件表达式"):
            run_yaml_instance._safe_eval_condition("os.system('ls')")


class TestSafeGetFunction:
    """测试安全函数获取功能"""

    @pytest.fixture
    def run_yaml_instance(self):
        """创建RunYaml实例用于测试"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

        from runner import RunYaml

        raw = {'config': {'name': 'test'}}
        module = types.ModuleType('test_module')
        g = {}

        run_yaml = RunYaml(raw, module, g, validate_config=False)

        # 添加一些安全的函数到context
        run_yaml.context['safe_func'] = lambda x: x * 2
        run_yaml.context['another_func'] = lambda: "hello"

        return run_yaml

    def test_get_existing_function(self, run_yaml_instance):
        """测试获取已存在的函数"""
        func = run_yaml_instance._safe_get_function('safe_func')
        assert callable(func)
        assert func(5) == 10

    def test_get_nonexistent_function(self, run_yaml_instance):
        """测试获取不存在的函数"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="未找到函数"):
            run_yaml_instance._safe_get_function('nonexistent_func')

    def test_get_non_callable_value(self, run_yaml_instance):
        """测试获取非可调用对象"""
        from exceptions import ParserError

        run_yaml_instance.context['not_a_func'] = 42

        with pytest.raises(ParserError, match="不是可调用的函数"):
            run_yaml_instance._safe_get_function('not_a_func')

    def test_dangerous_function_name_with_dot(self, run_yaml_instance):
        """测试包含点号的危险函数名"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的函数名"):
            run_yaml_instance._safe_get_function('os.system')

    def test_dangerous_function_name_with_parenthesis(self, run_yaml_instance):
        """测试包含括号的危险函数名"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的函数名"):
            run_yaml_instance._safe_get_function('func()')

    def test_dangerous_function_name_with_import(self, run_yaml_instance):
        """测试包含import的危险函数名"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="不安全的函数名"):
            run_yaml_instance._safe_get_function('import os')

    def test_non_string_function_name(self, run_yaml_instance):
        """测试非字符串函数名"""
        from exceptions import ParserError

        with pytest.raises(ParserError, match="函数名必须是字符串类型"):
            run_yaml_instance._safe_get_function(123)


class TestSQLInjectionProtection:
    """测试SQL注入防护"""

    @pytest.fixture
    def mock_db_without_connection(self):
        """创建不实际连接数据库的模拟对象"""
        from db import ConnectMysql
        db = ConnectMysql.__new__(ConnectMysql)
        db.host = "localhost"
        db.user = "test"
        db.password = "test"
        db.port = 3306
        db.database = "test_db"
        db.connection = None
        return db

    def test_validate_safe_sql(self, mock_db_without_connection):
        """测试验证安全的SQL"""
        # 这些SQL应该是安全的
        mock_db_without_connection._validate_sql("SELECT * FROM users WHERE id = %s")
        mock_db_without_connection._validate_sql("INSERT INTO users (name) VALUES (%s)")
        mock_db_without_connection._validate_sql("UPDATE users SET name = %s WHERE id = %s")

    def test_validate_dangerous_drop_table(self, mock_db_without_connection):
        """测试检测DROP TABLE"""
        with pytest.raises(ValueError, match="危险的SQL操作"):
            mock_db_without_connection._validate_sql("DROP TABLE users")

    def test_validate_dangerous_delete_all(self, mock_db_without_connection):
        """测试检测无条件的DELETE"""
        with pytest.raises(ValueError, match="危险的SQL操作"):
            mock_db_without_connection._validate_sql("DELETE FROM users")

    def test_validate_safe_delete_with_where(self, mock_db_without_connection):
        """测试安全的DELETE（带WHERE）"""
        # 这应该是安全的，因为有WHERE条件
        mock_db_without_connection._validate_sql("DELETE FROM users WHERE id = %s")

    def test_validate_dangerous_truncate(self, mock_db_without_connection):
        """测试检测TRUNCATE"""
        with pytest.raises(ValueError, match="危险的SQL操作"):
            mock_db_without_connection._validate_sql("TRUNCATE TABLE users")

    def test_sanitize_sql_with_placeholders(self, mock_db_without_connection):
        """测试带占位符的SQL清理"""
        sql, params = mock_db_without_connection._sanitize_sql(
            "SELECT * FROM users WHERE id = %s",
            (123,)
        )
        assert sql == "SELECT * FROM users WHERE id = %s"
        assert params == (123,)

    def test_sanitize_sql_with_single_param(self, mock_db_without_connection):
        """测试单个参数的清理"""
        sql, params = mock_db_without_connection._sanitize_sql(
            "SELECT * FROM users WHERE id = %s",
            123
        )
        assert sql == "SELECT * FROM users WHERE id = %s"
        assert params == (123,)

    def test_sanitize_sql_without_params(self, mock_db_without_connection):
        """测试不带参数的SQL清理"""
        sql, params = mock_db_without_connection._sanitize_sql(
            "SELECT * FROM users",
            None
        )
        assert sql == "SELECT * FROM users"
        assert params == ()


class TestYAMLValidator:
    """测试YAML配置验证器"""

    @pytest.fixture
    def validator(self):
        """创建验证器实例"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

        from yaml_validator import YAMLConfigValidator
        return YAMLConfigValidator()

    def test_valid_minimal_config(self, validator):
        """测试有效的最小配置"""
        config = {
            'config': {
                'name': 'test',
                'base_url': 'https://api.example.com'
            }
        }
        assert validator.validate_config(config) is True

    def test_missing_both_config_and_tests(self, validator):
        """测试缺少config和tests"""
        from exceptions import ConfigError

        config = {'other': 'data'}

        with pytest.raises(ConfigError):
            validator.validate_config(config)

    def test_invalid_timeout(self, validator):
        """测试无效的timeout"""
        from exceptions import ConfigError

        config = {
            'config': {
                'timeout': -1
            }
        }

        with pytest.raises(ConfigError):
            validator.validate_config(config)

    def test_invalid_base_url_type(self, validator):
        """测试无效的base_url类型"""
        from exceptions import ConfigError

        config = {
            'config': {
                'base_url': 123
            }
        }

        with pytest.raises(ConfigError):
            validator.validate_config(config)

    def test_invalid_http_method(self, validator):
        """测试无效的HTTP方法"""
        from exceptions import ConfigError

        config = {
            'config': {},
            'tests': [
                {
                    'name': 'test',
                    'request': {
                        'method': 'INVALID_METHOD',
                        'url': '/test'
                    }
                }
            ]
        }

        with pytest.raises(ConfigError):
            validator.validate_config(config)

    def test_missing_url_in_http_request(self, validator):
        """测试HTTP请求缺少URL"""
        from exceptions import ConfigError

        config = {
            'config': {},
            'tests': [
                {
                    'name': 'test',
                    'request': {
                        'method': 'GET'
                    }
                }
            ]
        }

        with pytest.raises(ConfigError):
            validator.validate_config(config)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
