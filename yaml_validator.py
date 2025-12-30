"""
YAML配置验证器

提供YAML配置文件的Schema验证功能，确保配置格式正确。
"""

from typing import Dict, Any, List, Optional, Union
import yaml
from pathlib import Path
from logging_config import get_logger
import exceptions

log = get_logger()


class YAMLConfigValidator:
    """YAML配置验证器"""

    # 支持的HTTP方法
    VALID_HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']

    # 支持的验证操作符
    VALID_OPERATORS = [
        'eq', 'ne', 'gt', 'lt', 'ge', 'le',
        'in', 'not_in', 'contains', 'not_contains',
        'regex', 'not_regex', 'less_than', 'greater_than',
        'custom', 'type', 'length', 'exists', 'not_exists'
    ]

    # 支持的请求类型
    VALID_REQUEST_TYPES = ['http', 'websocket', 'socket', 'graphql', 'grpc']

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_file(self, file_path: Union[str, Path]) -> bool:
        """
        验证YAML配置文件

        Args:
            file_path: YAML文件路径

        Returns:
            验证是否通过

        Raises:
            FileError: 文件不存在或无法读取
            ParserError: YAML解析失败
            ConfigError: 配置验证失败
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise exceptions.FileError(f"配置文件不存在: {file_path}")

        if not file_path.is_file():
            raise exceptions.FileError(f"路径不是文件: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise exceptions.ParserError(f"YAML解析失败: {e}")
        except Exception as e:
            raise exceptions.FileError(f"读取文件失败: {e}")

        return self.validate_config(config, file_path=str(file_path))

    def validate_config(self, config: Dict[str, Any], file_path: str = "") -> bool:
        """
        验证配置字典

        Args:
            config: 配置字典
            file_path: 文件路径（用于错误消息）

        Returns:
            验证是否通过

        Raises:
            ConfigError: 配置验证失败
        """
        self.errors = []
        self.warnings = []

        if not isinstance(config, dict):
            raise exceptions.ConfigError("配置必须是字典类型")

        # 验证顶层结构
        self._validate_top_level(config)

        # 验证config部分
        if 'config' in config:
            self._validate_config_section(config['config'])

        # 验证tests部分
        if 'tests' in config:
            self._validate_tests_section(config['tests'])

        # 检查是否有测试用例
        has_tests = False
        for key in config.keys():
            if key.startswith('test') or key == 'tests':
                has_tests = True
                if isinstance(config[key], list):
                    self._validate_test_cases(config[key], section=key)

        if not has_tests:
            self.warnings.append("配置中未找到测试用例")

        # 如果有错误，抛出异常
        if self.errors:
            error_msg = f"配置验证失败 ({len(self.errors)} 个错误)"
            if file_path:
                error_msg += f" - 文件: {file_path}"
            error_msg += "\n" + "\n".join(f"  - {err}" for err in self.errors)
            raise exceptions.ConfigError(error_msg)

        # 记录警告
        if self.warnings:
            log.warning(f"配置验证警告 ({len(self.warnings)} 个):")
            for warning in self.warnings:
                log.warning(f"  - {warning}")

        return True

    def _validate_top_level(self, config: Dict[str, Any]):
        """验证顶层配置结构"""
        # 检查是否有config或tests
        if 'config' not in config and not any(k.startswith('test') for k in config.keys()):
            self.errors.append("配置必须包含 'config' 或 'tests' 部分")

    def _validate_config_section(self, config: Dict[str, Any]):
        """验证config部分"""
        if not isinstance(config, dict):
            self.errors.append("config 必须是字典类型")
            return

        # 验证base_url（可选但推荐）
        if 'base_url' in config:
            base_url = config['base_url']
            if not isinstance(base_url, str):
                self.errors.append("config.base_url 必须是字符串类型")
            elif not (base_url.startswith('http://') or base_url.startswith('https://')):
                self.warnings.append(f"config.base_url 建议使用完整URL: {base_url}")

        # 验证timeout
        if 'timeout' in config:
            timeout = config['timeout']
            if not isinstance(timeout, (int, float)):
                self.errors.append("config.timeout 必须是数字类型")
            elif timeout <= 0:
                self.errors.append("config.timeout 必须大于0")

        # 验证retry_count
        if 'retry_count' in config:
            retry_count = config['retry_count']
            if not isinstance(retry_count, int):
                self.errors.append("config.retry_count 必须是整数类型")
            elif retry_count < 0:
                self.errors.append("config.retry_count 不能为负数")

        # 验证headers
        if 'headers' in config:
            if not isinstance(config['headers'], dict):
                self.errors.append("config.headers 必须是字典类型")

        # 验证variables
        if 'variables' in config:
            if not isinstance(config['variables'], dict):
                self.errors.append("config.variables 必须是字典类型")

        # 验证export
        if 'export' in config:
            if not isinstance(config['export'], list):
                self.errors.append("config.export 必须是列表类型")

    def _validate_tests_section(self, tests: Any):
        """验证tests部分"""
        if isinstance(tests, list):
            self._validate_test_cases(tests, section='tests')
        else:
            self.errors.append("tests 必须是列表类型")

    def _validate_test_cases(self, test_cases: List[Dict], section: str = "tests"):
        """验证测试用例列表"""
        if not isinstance(test_cases, list):
            self.errors.append(f"{section} 必须是列表类型")
            return

        for idx, test_case in enumerate(test_cases):
            self._validate_single_test_case(test_case, f"{section}[{idx}]")

    def _validate_single_test_case(self, test_case: Dict[str, Any], path: str):
        """验证单个测试用例"""
        if not isinstance(test_case, dict):
            self.errors.append(f"{path}: 测试用例必须是字典类型")
            return

        # 验证name（可选但推荐）
        if 'name' not in test_case:
            self.warnings.append(f"{path}: 建议添加 'name' 字段")
        elif not isinstance(test_case['name'], str):
            self.errors.append(f"{path}.name: 必须是字符串类型")

        # 验证request（必需）
        if 'request' not in test_case:
            self.errors.append(f"{path}: 缺少必需的 'request' 字段")
        else:
            self._validate_request(test_case['request'], f"{path}.request")

        # 验证validate（可选）
        if 'validate' in test_case:
            self._validate_validations(test_case['validate'], f"{path}.validate")

        # 验证extract（可选）
        if 'extract' in test_case:
            self._validate_extractions(test_case['extract'], f"{path}.extract")

    def _validate_request(self, request: Dict[str, Any], path: str):
        """验证request部分"""
        if not isinstance(request, dict):
            self.errors.append(f"{path}: request 必须是字典类型")
            return

        # 验证method（必需）
        if 'method' not in request and 'type' not in request:
            self.errors.append(f"{path}: 缺少 'method' 或 'type' 字段")
        elif 'method' in request:
            method = request['method']
            if not isinstance(method, str):
                self.errors.append(f"{path}.method: 必须是字符串类型")
            elif method.upper() not in self.VALID_HTTP_METHODS:
                self.errors.append(
                    f"{path}.method: 不支持的HTTP方法 '{method}'，"
                    f"支持的方法: {', '.join(self.VALID_HTTP_METHODS)}"
                )

        # 验证url（必需，除非是websocket/socket类型）
        request_type = request.get('type', 'http')
        if request_type in ['http', 'graphql']:
            if 'url' not in request:
                self.errors.append(f"{path}: 缺少必需的 'url' 字段")
            elif not isinstance(request['url'], str):
                self.errors.append(f"{path}.url: 必须是字符串类型")

        # 验证headers
        if 'headers' in request and not isinstance(request['headers'], dict):
            self.errors.append(f"{path}.headers: 必须是字典类型")

        # 验证params
        if 'params' in request and not isinstance(request['params'], dict):
            self.errors.append(f"{path}.params: 必须是字典类型")

        # 验证json和data不能同时存在
        if 'json' in request and 'data' in request:
            self.warnings.append(f"{path}: 同时指定了 'json' 和 'data'，将使用 'json'")

    def _validate_validations(self, validations: Any, path: str):
        """验证validate部分"""
        if not isinstance(validations, list):
            self.errors.append(f"{path}: validate 必须是列表类型")
            return

        for idx, validation in enumerate(validations):
            self._validate_single_validation(validation, f"{path}[{idx}]")

    def _validate_single_validation(self, validation: Dict[str, Any], path: str):
        """验证单个验证规则"""
        if not isinstance(validation, dict):
            self.errors.append(f"{path}: 验证规则必须是字典类型")
            return

        # 验证check（必需）
        if 'check' not in validation:
            self.errors.append(f"{path}: 缺少必需的 'check' 字段")

        # 验证expected或operator
        if 'expected' not in validation and 'operator' not in validation:
            self.warnings.append(f"{path}: 建议添加 'expected' 或 'operator' 字段")

        # 验证operator
        if 'operator' in validation:
            operator = validation['operator']
            if not isinstance(operator, str):
                self.errors.append(f"{path}.operator: 必须是字符串类型")
            elif operator not in self.VALID_OPERATORS and operator not in ['<', '>', '<=', '>=', '==', '!=']:
                self.warnings.append(
                    f"{path}.operator: 不常见的操作符 '{operator}'，"
                    f"支持的操作符: {', '.join(self.VALID_OPERATORS)}"
                )

    def _validate_extractions(self, extractions: Any, path: str):
        """验证extract部分"""
        if isinstance(extractions, dict):
            # 字典格式: {变量名: 提取表达式}
            for key, value in extractions.items():
                if not isinstance(key, str):
                    self.errors.append(f"{path}.{key}: 变量名必须是字符串")
        elif isinstance(extractions, list):
            # 列表格式
            for idx, extraction in enumerate(extractions):
                if isinstance(extraction, dict):
                    if 'name' not in extraction:
                        self.warnings.append(f"{path}[{idx}]: 建议添加 'name' 字段")
                else:
                    self.errors.append(f"{path}[{idx}]: 提取规则必须是字典类型")
        else:
            self.errors.append(f"{path}: extract 必须是字典或列表类型")

    def get_validation_report(self) -> Dict[str, Any]:
        """获取验证报告"""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
        }


def validate_yaml_file(file_path: Union[str, Path]) -> bool:
    """
    验证YAML配置文件（便捷函数）

    Args:
        file_path: YAML文件路径

    Returns:
        验证是否通过
    """
    validator = YAMLConfigValidator()
    return validator.validate_file(file_path)


def validate_yaml_config(config: Dict[str, Any]) -> bool:
    """
    验证YAML配置字典（便捷函数）

    Args:
        config: 配置字典

    Returns:
        验证是否通过
    """
    validator = YAMLConfigValidator()
    return validator.validate_config(config)


if __name__ == '__main__':
    # 测试验证器
    print("测试YAML配置验证器...")

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
    try:
        result = validator.validate_config(valid_config)
        print(f"✅ 有效配置验证通过: {result}")
    except Exception as e:
        print(f"❌ 验证失败: {e}")

    # 测试无效配置
    invalid_config = {
        'config': {
            'timeout': -1,  # 无效的timeout
        },
        'tests': [
            {
                'request': {
                    'method': 'INVALID_METHOD',  # 无效的方法
                }
            }
        ]
    }

    validator2 = YAMLConfigValidator()
    try:
        validator2.validate_config(invalid_config)
        print("❌ 应该抛出异常但没有")
    except exceptions.ConfigError as e:
        print(f"✅ 正确捕获配置错误: {e}")

    print("\n验证报告:")
    report = validator2.get_validation_report()
    print(f"错误数: {report['error_count']}")
    print(f"警告数: {report['warning_count']}")
