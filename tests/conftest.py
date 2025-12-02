"""
Pytest配置文件
定义fixtures和测试配置
"""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def test_config():
    """测试配置"""
    return {
        "base_url": "https://httpbin.org",
        "timeout": 30,
        "retry_count": 3
    }
