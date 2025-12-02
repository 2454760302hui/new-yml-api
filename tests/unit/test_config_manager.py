"""
配置管理器单元测试
Unit Tests for Configuration Manager
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config_manager import ConfigManager, TestEnv, ProdEnv, LocalEnv


class TestConfigManager:
    """测试配置管理器"""
    
    def test_init_with_test_env(self):
        """测试初始化测试环境"""
        config = ConfigManager(env="test")
        assert config.env == "test"
        assert config.get_base_url() == "https://httpbin.org"
    
    def test_init_with_prod_env(self):
        """测试初始化生产环境"""
        config = ConfigManager(env="prod")
        assert config.env == "prod"
    
    def test_init_with_local_env(self):
        """测试初始化本地环境"""
        config = ConfigManager(env="local")
        assert config.env == "local"
    
    def test_get_base_url(self):
        """测试获取基础URL"""
        config = ConfigManager(env="test")
        base_url = config.get_base_url()
        assert isinstance(base_url, str)
        assert len(base_url) > 0
    
    def test_get_timeout(self):
        """测试获取超时时间"""
        config = ConfigManager(env="test")
        timeout = config.get_timeout()
        assert isinstance(timeout, int)
        assert timeout > 0
    
    def test_get_retry_count(self):
        """测试获取重试次数"""
        config = ConfigManager(env="test")
        retry_count = config.get_retry_count()
        assert isinstance(retry_count, int)
        assert retry_count >= 0
    
    def test_set_and_get_config(self):
        """测试设置和获取配置"""
        config = ConfigManager(env="test")
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"
    
    def test_get_with_default(self):
        """测试获取不存在的配置返回默认值"""
        config = ConfigManager(env="test")
        value = config.get("non_existent_key", "default_value")
        assert value == "default_value"
    
    def test_to_dict(self):
        """测试转换为字典"""
        config = ConfigManager(env="test")
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
    
    def test_update_from_dict(self):
        """测试从字典更新配置"""
        config = ConfigManager(env="test")
        update_dict = {
            "key1": "value1",
            "key2": "value2"
        }
        config.update_from_dict(update_dict)
        assert config.get("key1") == "value1"
        assert config.get("key2") == "value2"


class TestEnvironmentConfigs:
    """测试环境配置类"""
    
    def test_test_env_attributes(self):
        """测试测试环境配置属性"""
        assert hasattr(TestEnv, 'BASE_URL')
        assert hasattr(TestEnv, 'TIMEOUT')
    
    def test_prod_env_attributes(self):
        """测试生产环境配置属性"""
        assert hasattr(ProdEnv, 'BASE_URL')
        assert hasattr(ProdEnv, 'TIMEOUT')
    
    def test_local_env_attributes(self):
        """测试本地环境配置属性"""
        assert hasattr(LocalEnv, 'BASE_URL')
        assert hasattr(LocalEnv, 'TIMEOUT')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
