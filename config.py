"""
YH API测试框架 - 配置文件
Configuration File for YH API Testing Framework

提供默认配置和环境配置管理
"""

import os
from pathlib import Path


class BaseConfig:
    """基础配置类"""
    
    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent
    
    # 默认测试文件
    DEFAULT_TEST_FILE = "default_test.yaml"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 报告配置
    ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"
    ALLURE_REPORT_DIR = PROJECT_ROOT / "allure-report"
    
    # 超时配置
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRY_COUNT = 3
    
    # 并发配置
    MAX_WORKERS = 5
    
    # 文档服务器配置
    DOCS_SERVER_HOST = "127.0.0.1"
    DOCS_SERVER_PORT = 8080


class TestEnv(BaseConfig):
    """测试环境配置"""
    
    ENV_NAME = "test"
    BASE_URL = os.getenv("TEST_BASE_URL", "https://httpbin.org")
    
    # 数据库配置（可选）
    MYSQL_HOST = os.getenv("TEST_MYSQL_HOST", "")
    MYSQL_PORT = int(os.getenv("TEST_MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("TEST_MYSQL_USER", "")
    MYSQL_PASSWORD = os.getenv("TEST_MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("TEST_MYSQL_DATABASE", "")
    
    # Redis配置（可选）
    REDIS_HOST = os.getenv("TEST_REDIS_HOST", "")
    REDIS_PORT = int(os.getenv("TEST_REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("TEST_REDIS_PASSWORD", "")
    REDIS_DB = int(os.getenv("TEST_REDIS_DB", "0"))


class ProdEnv(BaseConfig):
    """生产环境配置"""
    
    ENV_NAME = "prod"
    BASE_URL = os.getenv("PROD_BASE_URL", "https://api.production.com")
    
    # 生产环境超时时间更长
    DEFAULT_TIMEOUT = 60
    DEFAULT_RETRY_COUNT = 5
    
    # 数据库配置（可选）
    MYSQL_HOST = os.getenv("PROD_MYSQL_HOST", "")
    MYSQL_PORT = int(os.getenv("PROD_MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("PROD_MYSQL_USER", "")
    MYSQL_PASSWORD = os.getenv("PROD_MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("PROD_MYSQL_DATABASE", "")
    
    # Redis配置（可选）
    REDIS_HOST = os.getenv("PROD_REDIS_HOST", "")
    REDIS_PORT = int(os.getenv("PROD_REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("PROD_REDIS_PASSWORD", "")
    REDIS_DB = int(os.getenv("PROD_REDIS_DB", "0"))


class LocalEnv(BaseConfig):
    """本地开发环境配置"""
    
    ENV_NAME = "local"
    BASE_URL = os.getenv("LOCAL_BASE_URL", "http://localhost:8000")
    
    # 本地环境超时时间较短
    DEFAULT_TIMEOUT = 10
    DEFAULT_RETRY_COUNT = 1
    
    # 数据库配置（可选）
    MYSQL_HOST = os.getenv("LOCAL_MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("LOCAL_MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("LOCAL_MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("LOCAL_MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("LOCAL_MYSQL_DATABASE", "test_db")
    
    # Redis配置（可选）
    REDIS_HOST = os.getenv("LOCAL_REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("LOCAL_REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.getenv("LOCAL_REDIS_PASSWORD", "")
    REDIS_DB = int(os.getenv("LOCAL_REDIS_DB", "0"))


# 环境配置映射
ENV_CONFIG_MAP = {
    "test": TestEnv,
    "prod": ProdEnv,
    "local": LocalEnv,
}


def get_config(env_name: str = None):
    """
    获取配置对象
    
    Args:
        env_name: 环境名称，默认从环境变量YH_ENV读取，否则使用test
    
    Returns:
        配置类
    """
    if env_name is None:
        env_name = os.getenv("YH_ENV", "test")
    
    config_class = ENV_CONFIG_MAP.get(env_name, TestEnv)
    return config_class


# 默认配置（向后兼容）
config = get_config()
