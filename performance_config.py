"""
性能优化配置模块
Performance Optimization Configuration Module

优化项目性能的核心配置
"""

import os
import logging

# ============================================
# HTTP 性能优化配置
# ============================================

HTTP_PERFORMANCE_CONFIG = {
    # 连接池配置
    'pool_connections': 50,      # 增加连接池大小（默认10）
    'pool_maxsize': 100,         # 增加最大连接数（默认10）
    'max_retries': 3,            # 重试次数
    'pool_block': False,         # 非阻塞模式
    
    # 超时配置（秒）
    'timeout': {
        'connect': 5,            # 连接超时
        'read': 10,              # 读取超时
    },
    
    # Keep-Alive 配置
    'keep_alive': True,          # 启用连接复用
    'keep_alive_timeout': 30,    # Keep-Alive 超时时间
}

# ============================================
# 并发测试配置
# ============================================

CONCURRENT_CONFIG = {
    'max_workers': os.cpu_count() * 2,  # 线程池大小（CPU核心数 x 2）
    'chunk_size': 10,                    # 批处理大小
    'enable_async': True,                # 启用异步模式
}

# ============================================
# 缓存配置
# ============================================

CACHE_CONFIG = {
    'enable_response_cache': False,      # 响应缓存（开发时关闭）
    'cache_ttl': 300,                    # 缓存有效期（秒）
    'max_cache_size': 100,               # 最大缓存条目
}

# ============================================
# 日志性能优化
# ============================================

LOGGING_CONFIG = {
    'level': logging.INFO,               # 生产环境使用 INFO
    'enable_file_logging': True,         # 启用文件日志
    'log_rotation': True,                # 日志轮转
    'max_bytes': 10 * 1024 * 1024,      # 单个日志文件最大 10MB
    'backup_count': 5,                   # 保留5个备份
    'buffer_size': 8192,                 # 增加缓冲区大小
}

# ============================================
# 数据库连接池配置（可选）
# ============================================

DB_POOL_CONFIG = {
    'mysql': {
        'pool_size': 10,                 # 连接池大小
        'max_overflow': 20,              # 最大溢出连接
        'pool_timeout': 30,              # 连接超时
        'pool_recycle': 3600,            # 连接回收时间（1小时）
    },
    'redis': {
        'max_connections': 50,           # 最大连接数
        'socket_keepalive': True,        # 启用 TCP keepalive
        'socket_connect_timeout': 5,     # 连接超时
        'decode_responses': True,        # 自动解码响应
    }
}

# ============================================
# 内存优化配置
# ============================================

MEMORY_CONFIG = {
    'enable_gc': True,                   # 启用垃圾回收
    'gc_threshold': (700, 10, 10),      # GC 阈值
    'clear_response_after_test': True,  # 测试后清理响应
}

# ============================================
# WebSocket 性能配置
# ============================================

WEBSOCKET_CONFIG = {
    'ping_interval': 20,                 # Ping 间隔（秒）
    'ping_timeout': 10,                  # Ping 超时（秒）
    'close_timeout': 10,                 # 关闭超时（秒）
    'max_size': 10 * 1024 * 1024,       # 最大消息大小 10MB
    'max_queue': 32,                     # 最大队列大小
}

# ============================================
# 性能监控配置
# ============================================

MONITOR_CONFIG = {
    'enable_profiling': False,           # 性能分析（开发环境启用）
    'enable_metrics': True,              # 启用指标收集
    'metrics_interval': 60,              # 指标收集间隔（秒）
    'track_memory': True,                # 跟踪内存使用
    'track_cpu': True,                   # 跟踪CPU使用
}

# ============================================
# 测试执行优化
# ============================================

TEST_EXECUTION_CONFIG = {
    'parallel_execution': True,          # 并行执行测试
    'rerun_failures': 2,                 # 失败重试次数
    'timeout_per_test': 300,             # 单个测试超时（5分钟）
    'early_stop_on_failure': False,      # 遇错继续执行
}

# ============================================
# 导出配置函数
# ============================================

def get_optimized_http_config():
    """获取优化的HTTP配置"""
    return HTTP_PERFORMANCE_CONFIG

def get_concurrent_config():
    """获取并发配置"""
    return CONCURRENT_CONFIG

def get_all_performance_config():
    """获取所有性能配置"""
    return {
        'http': HTTP_PERFORMANCE_CONFIG,
        'concurrent': CONCURRENT_CONFIG,
        'cache': CACHE_CONFIG,
        'logging': LOGGING_CONFIG,
        'db_pool': DB_POOL_CONFIG,
        'memory': MEMORY_CONFIG,
        'websocket': WEBSOCKET_CONFIG,
        'monitor': MONITOR_CONFIG,
        'test_execution': TEST_EXECUTION_CONFIG,
    }

# ============================================
# 性能优化建议
# ============================================

PERFORMANCE_TIPS = """
🚀 性能优化建议

1. HTTP请求优化
   - 使用连接池（已配置）
   - 启用 Keep-Alive（已配置）
   - 合理设置超时时间

2. 并发测试优化
   - max_workers = CPU核心数 x 2（已配置）
   - 使用线程池而非多进程（I/O密集）
   - 批量处理请求

3. 内存优化
   - 及时清理响应对象
   - 使用生成器处理大数据
   - 定期执行垃圾回收

4. 日志优化
   - 生产环境使用 INFO 级别
   - 启用日志轮转
   - 使用异步日志（可选）

5. 数据库优化
   - 使用连接池
   - 批量操作
   - 索引优化

6. 依赖优化
   - 仅安装必要依赖
   - 使用 --no-cache-dir 安装
   - 定期清理未使用包

7. 代码优化
   - 延迟导入（lazy import）
   - 避免重复计算
   - 使用缓存装饰器
"""

if __name__ == "__main__":
    import json
    print("=" * 60)
    print("性能配置概览")
    print("=" * 60)
    config = get_all_performance_config()
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("\n" + PERFORMANCE_TIPS)
