"""
数据库连接模块
支持MySQL数据库操作
"""

import logging
from typing import List, Dict, Any, Optional

try:
    import pymysql
    from pymysql.cursors import DictCursor
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False

logger = logging.getLogger(__name__)


class ConnectMysql:
    """MySQL数据库连接类"""
    
    def __init__(self, host: str, user: str, password: str, 
                 port: int = 3306, database: str = None, **kwargs):
        """
        初始化MySQL连接
        
        Args:
            host: 数据库主机地址
            user: 用户名
            password: 密码
            port: 端口号
            database: 数据库名
        """
        if not PYMYSQL_AVAILABLE:
            raise ImportError("pymysql未安装，请执行: pip install pymysql")
        
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.connection = None
        self.connect()
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            logger.info(f"✅ 成功连接到MySQL: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"❌ MySQL连接失败: {e}")
            raise
    
    def query_sql(self, sql: str) -> List[Dict[str, Any]]:
        """
        查询SQL
        
        Args:
            sql: SQL查询语句
        
        Returns:
            查询结果列表
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                logger.info(f"✅ 查询成功: {len(result)}条记录")
                return result
        except Exception as e:
            logger.error(f"❌ 查询失败: {e}")
            raise
    
    def execute_sql(self, sql: str) -> int:
        """
        执行SQL（INSERT, UPDATE, DELETE等）
        
        Args:
            sql: SQL执行语句
        
        Returns:
            影响的行数
        """
        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(sql)
                self.connection.commit()
                logger.info(f"✅ 执行成功: 影响{affected_rows}行")
                return affected_rows
        except Exception as e:
            self.connection.rollback()
            logger.error(f"❌ 执行失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("✅ 数据库连接已关闭")
    
    def __del__(self):
        """析构函数，自动关闭连接"""
        self.close()
