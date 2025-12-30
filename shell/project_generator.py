#!/usr/bin/env python3
"""
YH Shell 项目生成器
生成完整的测试项目模板
"""

import os
from typing import Dict
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)


class ProjectGenerator:
    """项目生成器"""

    def __init__(self):
        pass

    @staticmethod
    def print_success(message: str):
        """打印成功消息"""
        print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")

    @staticmethod
    def print_info(message: str):
        """打印信息消息"""
        print(f"{Fore.CYAN}[DIR] {message}{Style.RESET_ALL}")

    def generate_test_project(self, project_name: str):
        """生成完整的测试项目"""
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=True)

        # 创建子目录
        (project_path / "config").mkdir(exist_ok=True)
        (project_path / "tests").mkdir(exist_ok=True)
        (project_path / "reports").mkdir(exist_ok=True)
        (project_path / "data").mkdir(exist_ok=True)
        (project_path / "utils").mkdir(exist_ok=True)

        self.print_info("创建项目目录结构...")

        # 生成各种配置和测试文件
        self._create_project_files(project_path)

        self.print_success("项目文件生成完成")

    def _create_project_files(self, project_path: Path):
        """创建项目文件"""
        self._create_main_config(project_path / "config" / "test_config.yaml")
        self._create_test_cases(project_path / "tests" / "api_tests.yaml")
        self._create_run_script(project_path / "run.py")
        self._create_readme(project_path / "README.md")
        self._create_env_config(project_path / "config" / "environments.yaml")
        self._create_test_data(project_path / "data" / "test_data.yaml")
        self._create_utils(project_path / "utils" / "helpers.py")

    def _create_main_config(self, config_path: Path):
        """创建主配置文件"""
        config_content = """# API测试框架配置文件
# 基础配置
base:
  name: "API测试项目"
  version: "1.0.0"
  description: "基于YH API测试框架的完整测试项目"

# 服务器配置
server:
  base_url: "https://httpbin.org"  # 替换为实际API地址
  timeout: 30
  retry_count: 3
  retry_delay: 1

# 认证配置
auth:
  type: "bearer"  # bearer, basic, api_key
  token: "your_api_token_here"  # 替换为实际token
  username: "test_user"
  password: "test_password"
  api_key_header: "X-API-Key"
  api_key_value: "your_api_key_here"

# 数据库配置（可选）
database:
  enabled: false
  host: "localhost"
  port: 5432
  name: "test_db"
  username: "db_user"
  password: "db_password"

# 报告配置
reporting:
  enabled: true
  formats: ["html", "json", "allure"]
  output_dir: "reports"
  include_screenshots: true

# 通知配置
notifications:
  wechat:
    enabled: false
    webhook_url: "your_wechat_webhook_url"
  email:
    enabled: false
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your_email@gmail.com"
    password: "your_email_password"
    recipients: ["recipient@example.com"]

# 并发配置
concurrency:
  max_workers: 5
  batch_size: 10
  delay_between_batches: 2

# 环境配置
environments:
  default: "test"
  available: ["dev", "test", "staging", "prod"]
"""

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        self.print_success(f"创建配置文件: {config_path.name}")

    def _create_test_cases(self, test_path: Path):
        """创建测试用例文件"""
        test_content = """# API测试用例集合
# 测试项目信息
project:
  name: "API接口测试"
  version: "1.0.0"
  description: "完整的API接口测试用例集合"

# 全局变量
globals:
  base_url: "https://httpbin.org"  # 替换为实际API地址
  api_version: "v1"
  content_type: "application/json"
  user_agent: "YH-API-Test-Framework/3.0"

# 测试用例
tests:
  # 1. 基础GET请求测试
  - name: "获取用户信息"
    description: "测试获取用户基本信息接口"
    method: "GET"
    url: "${base_url}/get"
    headers:
      Content-Type: "${content_type}"
      User-Agent: "${user_agent}"
    params:
      user_id: "12345"
      include_profile: true
    assertions:
      - type: "status_code"
        expected: 200
      - type: "response_time"
        expected: 2000
      - type: "json_path"
        path: "$.args.user_id"
        expected: "12345"

  # 2. POST请求测试
  - name: "创建新用户"
    description: "测试创建新用户接口"
    method: "POST"
    url: "${base_url}/post"
    headers:
      Content-Type: "${content_type}"
    data:
      name: "张三"
      email: "zhangsan@example.com"
      age: 25
      department: "技术部"
    assertions:
      - type: "status_code"
        expected: 200
      - type: "json_path"
        path: "$.json.name"
        expected: "张三"
      - type: "json_path"
        path: "$.json.email"
        expected: "zhangsan@example.com"

  # 3. PUT请求测试
  - name: "更新用户信息"
    description: "测试更新用户信息接口"
    method: "PUT"
    url: "${base_url}/put"
    headers:
      Content-Type: "${content_type}"
    data:
      name: "张三（已更新）"
      email: "zhangsan.updated@example.com"
      age: 26
    assertions:
      - type: "status_code"
        expected: 200
      - type: "json_path"
        path: "$.json.name"
        expected: "张三（已更新）"

  # 4. DELETE请求测试
  - name: "删除用户"
    description: "测试删除用户接口"
    method: "DELETE"
    url: "${base_url}/delete"
    headers:
      Content-Type: "${content_type}"
    params:
      user_id: "12345"
    assertions:
      - type: "status_code"
        expected: 200

  # 5. 文件上传测试
  - name: "上传文件"
    description: "测试文件上传接口"
    method: "POST"
    url: "${base_url}/post"
    files:
      file: "data/test_file.txt"
    data:
      description: "测试文件上传"
      category: "document"
    assertions:
      - type: "status_code"
        expected: 200
"""

        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        self.print_success(f"创建测试用例: {test_path.name}")

    def _create_run_script(self, script_path: Path):
        """创建运行脚本"""
        script_content = '''#!/usr/bin/env python3
"""
API测试项目运行脚本
使用YH API测试框架执行测试
"""

import os
import sys
import yaml
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)


def load_config():
    """加载配置文件"""
    config_path = Path("config/test_config.yaml")
    if not config_path.exists():
        print(f"{Fore.RED}[FAIL] 配置文件不存在: {config_path}{Style.RESET_ALL}")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_test_cases():
    """加载测试用例"""
    test_path = Path("tests/api_tests.yaml")
    if not test_path.exists():
        print(f"{Fore.RED}[FAIL] 测试用例文件不存在: {test_path}{Style.RESET_ALL}")
        return None

    with open(test_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def run_tests():
    """运行测试"""
    print(f"{Fore.YELLOW + Style.BRIGHT}[RUN] YH API测试框架 - 项目测试{Style.RESET_ALL}")
    print("=" * 60)

    config = load_config()
    if not config:
        return False

    test_cases = load_test_cases()
    if not test_cases:
        return False

    print(f"{Fore.CYAN}[INFO] 项目信息:{Style.RESET_ALL}")
    print(f"  名称: {test_cases.get('project', {}).get('name', 'Unknown')}")
    print(f"  版本: {test_cases.get('project', {}).get('version', '1.0.0')}")

    print(f"\\n{Fore.CYAN}[TOOL] 配置信息:{Style.RESET_ALL}")
    print(f"  基础URL: {config.get('server', {}).get('base_url', 'Not configured')}")

    return True


def main():
    """主函数"""
    success = run_tests()

    if success:
        print(f"\\n{Fore.GREEN + Style.BRIGHT}[SUCCESS] 测试执行完成！{Style.RESET_ALL}")
    else:
        print(f"\\n{Fore.RED}[FAIL] 测试执行失败{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
'''

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        self.print_success(f"创建运行脚本: {script_path.name}")

    def _create_readme(self, readme_path: Path):
        """创建README文档"""
        readme_content = '''# API测试项目

基于YH API测试框架的完整API测试项目模板。

## [RUN] 项目简介

这是一个使用YH API测试框架生成的完整测试项目，包含了完整的配置文件、测试用例、数据文件和工具类。

## [DIR] 项目结构

```
api_test_project/
├── config/                 # 配置文件目录
│   ├── test_config.yaml   # 主配置文件
│   └── environments.yaml  # 环境配置文件
├── tests/                  # 测试用例目录
│   └── api_tests.yaml     # API测试用例
├── data/                   # 测试数据目录
│   └── test_data.yaml     # 测试数据文件
├── utils/                  # 工具类目录
│   └── helpers.py         # 辅助工具类
├── reports/               # 测试报告目录
├── run.py                # 测试运行脚本
└── README.md             # 项目说明文档
```

## [RUN] 快速开始

### 1. 安装依赖

```bash
pip install api-test-yh-pro
```

### 2. 配置项目

编辑 `config/test_config.yaml` 文件，更新以下配置：
- `server.base_url`: 替换为实际的API服务器地址
- `auth`: 配置认证信息

### 3. 运行测试

```bash
python run.py
```

## [TIP] 使用技巧

1. **变量替换**: 在测试用例中使用 `${variable_name}` 进行变量替换
2. **数据提取**: 使用 `extract` 从响应中提取数据
3. **测试套件**: 使用 `suites` 组织不同类型的测试
4. **并发测试**: 配置 `concurrency` 进行并发测试

## 📞 支持

如有问题，请联系：
- QQ: 2677989813
'''

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        self.print_success(f"创建README文档: {readme_path.name}")

    def _create_env_config(self, env_path: Path):
        """创建环境配置文件"""
        env_content = '''# 环境配置文件
# 支持多环境配置，便于在不同环境间切换

# 开发环境
dev:
  name: "开发环境"
  base_url: "https://dev-api.example.com"
  database:
    host: "dev-db.example.com"
    port: 5432
    name: "dev_database"
  auth:
    token: "dev_token_here"

# 测试环境
test:
  name: "测试环境"
  base_url: "https://test-api.example.com"
  database:
    host: "test-db.example.com"
    port: 5432
    name: "test_database"
  auth:
    token: "test_token_here"

# 生产环境
prod:
  name: "生产环境"
  base_url: "https://api.example.com"
  database:
    host: "prod-db.example.com"
    port: 5432
    name: "prod_database"
  auth:
    token: "prod_token_here"
'''

        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        self.print_success(f"创建环境配置: {env_path.name}")

    def _create_test_data(self, data_path: Path):
        """创建测试数据文件"""
        data_content = '''# 测试数据文件
# 包含各种测试场景的数据

# 用户测试数据
users:
  valid_user:
    name: "张三"
    email: "zhangsan@example.com"
    age: 25
    department: "技术部"

  invalid_user:
    name: ""
    email: "invalid-email"
    age: -1

# 产品测试数据
products:
  valid_product:
    name: "测试产品"
    description: "这是一个测试产品"
    price: 99.99
    category: "电子产品"

  expensive_product:
    name: "高端产品"
    price: 9999.99
    category: "奢侈品"
'''

        with open(data_path, 'w', encoding='utf-8') as f:
            f.write(data_content)
        self.print_success(f"创建测试数据: {data_path.name}")

        # 创建测试文件
        test_file_path = data_path.parent / "test_file.txt"
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write("这是一个用于测试文件上传功能的示例文件。\\n")
        self.print_success(f"创建测试文件: {test_file_path.name}")

    def _create_utils(self, utils_path: Path):
        """创建工具类文件"""
        utils_content = '''#!/usr/bin/env python3
"""
测试辅助工具类
提供常用的测试工具函数
"""

import random
import string
from typing import Dict, Any, List


class TestHelpers:
    """测试辅助工具类"""

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_email() -> str:
        """生成随机邮箱地址"""
        username = TestHelpers.generate_random_string(8)
        domains = ['example.com', 'test.com', 'demo.org']
        return f"{username}@{random.choice(domains)}"


class DataGenerator:
    """测试数据生成器"""

    @staticmethod
    def generate_user_data(count: int = 1) -> List[Dict[str, Any]]:
        """生成用户测试数据"""
        users = []
        for i in range(count):
            user = {
                'id': i + 1,
                'name': f"测试用户{i+1:03d}",
                'email': TestHelpers.generate_random_email(),
                'age': random.randint(18, 65),
            }
            users.append(user)
        return users
'''

        with open(utils_path, 'w', encoding='utf-8') as f:
            f.write(utils_content)
        self.print_success(f"创建工具类: {utils_path.name}")
