# 🚀 YH API测试框架 - 快速开始指南

## 📦 安装

### 方式1️⃣: 最小安装（推荐新用户）

```bash
# 克隆项目
git clone https://github.com/your-repo/yh-api-test.git
cd yh-api-test

# 仅安装核心依赖（<1分钟）
pip install -r requirements.txt

# 验证安装
python yh_shell.py
```

**适合场景：**
- ✅ 快速体验框架
- ✅ 基础HTTP接口测试
- ✅ CI/CD环境

### 方式2️⃣: 完整安装

```bash
# 安装所有功能（5-10分钟）
pip install -r requirements-full.txt

# 或使用pyproject.toml
pip install .[full]
```

**适合场景：**
- ✅ 使用所有高级功能
- ✅ 开发和调试
- ✅ 本地完整环境

### 方式3️⃣: 按需安装（推荐企业用户）

```bash
# 核心功能
pip install -r requirements.txt

# 根据需要添加功能模块
pip install allure-pytest jinja2 lxml         # 报告功能
pip install fastapi uvicorn pydantic          # 文档服务器
pip install pymysql redis                     # 数据库支持
pip install websockets paramiko               # WebSocket/Socket
pip install faker pandas openpyxl             # 数据处理
```

---

## ⚡ 5分钟快速上手

### 步骤1: 启动Shell

```bash
python yh_shell.py
```

你会看到精美的欢迎界面：
```
╔═══════════════════════════════════════════════════════╗
║    🚀 API Testing                                     ║
║    ⚡ 智能 • 高效 • 专业                                ║
╚═══════════════════════════════════════════════════════╝

输入 'help' 查看所有命令
输入 'fadeaway' 开始你的API测试之旅
```

### 步骤2: 创建测试项目

```bash
🚀 YH-API-Test > generate my_first_test
```

这会创建一个完整的测试项目：
```
my_first_test/
├── config/
│   ├── test_config.yaml
│   └── environments.yaml
├── tests/
│   └── api_tests.yaml
├── data/
├── reports/
└── run.py
```

### 步骤3: 运行测试

```bash
🚀 YH-API-Test > load tests/api_tests.yaml
🚀 YH-API-Test > run
```

或使用便捷命令：
```bash
🚀 YH-API-Test > fadeaway tests/api_tests.yaml
```

---

## 📝 创建第一个测试

### 方式1: 使用YAML配置

创建 `my_test.yaml`：

```yaml
# 全局配置
config:
  name: "我的第一个API测试"
  base_url: "https://httpbin.org"

# 全局变量
variables:
  username: "testuser"
  password: "test123"

# 测试用例
tests:
  # 测试1: 简单GET请求
  - name: "GET请求测试"
    request:
      method: GET
      url: "/get"
      params:
        user: "${username}"
    validate:
      - check: status_code
        expected: 200
      - check: json.args.user
        expected: "${username}"

  # 测试2: POST请求
  - name: "POST请求测试"
    request:
      method: POST
      url: "/post"
      json:
        username: "${username}"
        password: "${password}"
    extract:
      response_data: json.data
    validate:
      - check: status_code
        expected: 200
      - check: json.json.username
        expected: "${username}"
```

### 方式2: 使用Python脚本

创建 `my_test.py`：

```python
from http_client import HttpClient

# 创建HTTP客户端
client = HttpClient(base_url="https://httpbin.org")

# 发送GET请求
response = client.get("/get", params={"name": "test"})
print(f"状态码: {response.status_code}")
print(f"响应: {response.json()}")

# 发送POST请求
response = client.post("/post", json={"key": "value"})
print(f"响应: {response.json()}")
```

---

## 🎯 常用命令速查

### Shell命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `help` | 显示帮助 | `help` |
| `load <file>` | 加载测试文件 | `load test.yaml` |
| `run` | 运行测试 | `run` |
| `fadeaway [file]` | 快速测试 | `fadeaway test.yaml` |
| `generate [name]` | 生成项目 | `generate my_project` |
| `vars` | 查看变量 | `vars` |
| `vars set <k> <v>` | 设置变量 | `vars set token abc123` |
| `status` | 查看状态 | `status` |
| `report` | 生成报告 | `report` |
| `docs` | 启动文档服务 | `docs` |
| `ai <url>` | AI智能测试 | `ai https://httpbin.org` |
| `exit` | 退出 | `exit` |

### Shell模式

所有命令都支持Shell模式：
```bash
🚀 YH-API-Test > shell run test.yaml
🚀 YH-API-Test > shell vars set token xyz
🚀 YH-API-Test > shell ai https://httpbin.org
```

---

## 🔧 配置环境

### 设置环境变量

**Linux/Mac:**
```bash
export YH_ENV=test
export TEST_BASE_URL=https://test-api.example.com
```

**Windows:**
```cmd
set YH_ENV=test
set TEST_BASE_URL=https://test-api.example.com
```

**或使用 `.env` 文件:**
```env
YH_ENV=test
TEST_BASE_URL=https://test-api.example.com
TEST_MYSQL_HOST=localhost
TEST_MYSQL_USER=root
```

### 多环境配置

```yaml
# config/environments.yaml
test:
  base_url: "https://test-api.example.com"
  timeout: 30

prod:
  base_url: "https://api.example.com"
  timeout: 60

local:
  base_url: "http://localhost:8000"
  timeout: 10
```

---

## 📊 查看测试报告

### 方式1: Allure报告（推荐）

```bash
# 在Shell中
🚀 YH-API-Test > report

# 或命令行
allure serve allure-results
```

### 方式2: 在线文档

```bash
# 启动文档服务器
🚀 YH-API-Test > docs

# 访问 http://127.0.0.1:8080
```

---

## 🤖 AI智能测试

框架内置AI智能测试功能：

```bash
# 自动发现和测试API
🚀 YH-API-Test > ai https://httpbin.org

# AI会自动：
# 1. 扫描API端点
# 2. 生成测试用例
# 3. 执行测试
# 4. 生成报告
```

---

## 💡 使用技巧

### 1. 快捷数字命令

```bash
🚀 YH-API-Test > 2    # 启动文档服务器
🚀 YH-API-Test > 6    # 生成测试项目
```

### 2. 变量引用

```yaml
variables:
  api_token: "abc123"
  user_id: "12345"

tests:
  - request:
      url: "/user/${user_id}"
      headers:
        Authorization: "Bearer ${api_token}"
```

### 3. 数据提取

```yaml
- name: "登录获取token"
  request:
    method: POST
    url: "/login"
    json:
      username: "admin"
      password: "secret"
  extract:
    token: json.data.token
    user_id: json.data.user.id

- name: "使用token访问"
  request:
    url: "/api/user/${user_id}"
    headers:
      Authorization: "Bearer ${token}"
```

### 4. 断言验证

```yaml
validate:
  # 状态码
  - check: status_code
    expected: 200
  
  # JSON路径
  - check: json.data.id
    expected: greater_than
    value: 0
  
  # 响应时间
  - check: response_time
    expected: less_than
    value: 2000
  
  # 正则匹配
  - check: json.email
    expected: regex
    pattern: "^[\\w.-]+@[\\w.-]+\\.\\w+$"
```

---

## 🆘 常见问题

### Q1: 安装依赖失败？
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 启动Shell报错？
```bash
# 检查Python版本（需要3.7+）
python --version

# 确保安装了核心依赖
pip install -r requirements.txt
```

### Q3: 如何调试测试？
```bash
# 使用详细模式
pytest test.yaml -v -s

# 查看日志
tail -f logs/test.log
```

### Q4: 报告生成失败？
```bash
# 安装报告依赖
pip install allure-pytest jinja2 lxml

# 或使用完整安装
pip install -r requirements-full.txt
```

---

## 📚 下一步

- 📖 阅读完整文档：[README.md](README.md)
- 🔍 查看改进说明：[IMPROVEMENTS.md](IMPROVEMENTS.md)
- 💻 查看示例项目：`examples/` 目录
- 🎯 运行综合测试：`python run_comprehensive_test.py`

---

## 📞 获取帮助

- **QQ技术支持**: 2677989813
- **GitHub Issues**: [提交问题](https://github.com/your-repo/issues)
- **在线文档**: 运行 `docs` 命令查看

---

**💪 YH精神永存！开始你的API测试之旅吧！** 🚀
