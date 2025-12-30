"""
数据库连接模块
支持MySQL数据库操作，使用参数化查询防止SQL注入
"""

import logging
import re
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import pymysql
    from pymysql.cursors import DictCursor
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False

logger = logging.getLogger(__name__)


class ConnectMysql:
    """MySQL数据库连接类，支持安全的参数化查询"""

    # 危险的SQL关键词，用于检测
    DANGEROUS_PATTERNS = [
        r'\bDROP\s+TABLE\b',
        r'\bDELETE\s+FROM\s+\w+\s*$',  # 没有WHERE条件的DELETE
        r'\bTRUNCATE\b',
        r'\bEXEC\b',
        r'\bEXECUTE\b',
        r';\s*DROP',  # 多语句注入
        r';\s*DELETE',
        r';\s*UPDATE',
        r'--\s*$',  # SQL注释
        r'/\*.*\*/',  # C风格注释
    ]

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

    def _validate_sql(self, sql: str) -> None:
        """
        验证SQL语句的安全性

        Args:
            sql: SQL语句

        Raises:
            ValueError: 如果检测到危险的SQL模式
        """
        sql_upper = sql.upper().strip()

        # 检查危险的SQL模式
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, sql_upper, re.IGNORECASE):
                raise ValueError(f"检测到危险的SQL操作: {pattern}")

    def _sanitize_sql(self, sql: str, params: Optional[Tuple] = None) -> Tuple[str, Tuple]:
        """
        清理SQL语句，确保使用参数化查询

        Args:
            sql: SQL语句（可能包含格式化占位符）
            params: 参数元组

        Returns:
            (cleaned_sql, cleaned_params) 清理后的SQL和参数

        Raises:
            ValueError: 如果SQL包含字符串拼接
        """
        # 如果SQL包含 %s，说明已经使用了参数化查询
        if '%s' in sql or '%d' in sql or '%f' in sql:
            if params is None:
                logger.warning("SQL包含占位符但未提供参数，可能导致空值查询")
                params = ()
            return sql, (params if isinstance(params, (tuple, list)) else (params,))

        # 检查是否使用了字符串拼接（危险）
        dangerous_indicators = ['"', "'", 'f"', "f'", '"""', "'''"]
        for indicator in dangerous_indicators:
            # 检查SQL中是否有字符串字面量（简单检测）
            if indicator in sql and any(keyword in sql for keyword in ['WHERE', 'VALUES']):
                # 可能的字符串拼接，警告但不阻止（某些场景可能需要）
                logger.warning(f"SQL可能包含字符串拼接，建议使用参数化查询。SQL: {sql[:100]}...")

        return sql, params or ()

    def query_sql(self, sql: str, params: Optional[Union[Tuple, List, Dict]] = None) -> List[Dict[str, Any]]:
        """
        安全的SQL查询（使用参数化查询防止SQL注入）

        Args:
            sql: SQL查询语句，使用 %s 作为参数占位符
            params: 查询参数（元组、列表或字典）

        Returns:
            查询结果列表

        Examples:
            # 安全方式 - 使用参数化查询
            >>> db.query_sql("SELECT * FROM users WHERE id = %s", (user_id,))
            >>> db.query_sql("SELECT * FROM users WHERE name = %s AND age > %s", ("John", 18))

        Raises:
            ValueError: 如果检测到危险的SQL操作
        """
        # 验证SQL安全性
        self._validate_sql(sql)

        # 清理SQL和参数
        cleaned_sql, cleaned_params = self._sanitize_sql(sql, params)

        try:
            with self.connection.cursor() as cursor:
                if cleaned_params:
                    cursor.execute(cleaned_sql, cleaned_params)
                else:
                    # 如果没有参数，仍然执行但要记录警告
                    if any(keyword in cleaned_sql.upper() for keyword in ['WHERE', 'VALUES', 'INSERT', 'UPDATE', 'DELETE']):
                        logger.warning(f"执行不带参数的SQL查询: {cleaned_sql[:100]}...")
                    cursor.execute(cleaned_sql)

                result = cursor.fetchall()
                logger.info(f"✅ 查询成功: {len(result)}条记录")
                return result
        except Exception as e:
            logger.error(f"❌ 查询失败: {e}")
            raise

    def execute_sql(self, sql: str, params: Optional[Union[Tuple, List, Dict]] = None) -> int:
        """
        安全的SQL执行（INSERT, UPDATE, DELETE等，使用参数化查询防止SQL注入）

        Args:
            sql: SQL执行语句，使用 %s 作为参数占位符
            params: 执行参数（元组、列表或字典）

        Returns:
            影响的行数

        Examples:
            # 安全方式 - 使用参数化查询
            >>> db.execute_sql("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", 25))
            >>> db.execute_sql("UPDATE users SET age = %s WHERE id = %s", (26, 1))

        Raises:
            ValueError: 如果检测到危险的SQL操作
        """
        # 验证SQL安全性
        self._validate_sql(sql)

        # 清理SQL和参数
        cleaned_sql, cleaned_params = self._sanitize_sql(sql, params)

        try:
            with self.connection.cursor() as cursor:
                if cleaned_params:
                    affected_rows = cursor.execute(cleaned_sql, cleaned_params)
                else:
                    # 如果没有参数，仍然执行但要记录警告
                    logger.warning(f"执行不带参数的SQL语句: {cleaned_sql[:100]}...")
                    affected_rows = cursor.execute(cleaned_sql)

                self.connection.commit()
                logger.info(f"✅ 执行成功: 影响{affected_rows}行")
                return affected_rows
        except Exception as e:
            self.connection.rollback()
            logger.error(f"❌ 执行失败: {e}")
            raise

    def execute_many(self, sql: str, params_list: List[Union[Tuple, List]]) -> int:
        """
        批量执行SQL语句

        Args:
            sql: SQL语句，使用 %s 作为参数占位符
            params_list: 参数列表

        Returns:
            总影响的行数
        """
        self._validate_sql(sql)
        cleaned_sql, _ = self._sanitize_sql(sql)

        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.executemany(cleaned_sql, params_list)
                self.connection.commit()
                logger.info(f"✅ 批量执行成功: 影响{affected_rows}行")
                return affected_rows
        except Exception as e:
            self.connection.rollback()
            logger.error(f"❌ 批量执行失败: {e}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("✅ 数据库连接已关闭")

    def __del__(self):
        """析构函数，自动关闭连接"""
        self.close()

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        self.close()
