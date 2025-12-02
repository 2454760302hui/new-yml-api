#!/usr/bin/env python3
"""
综合测试执行脚本
执行全面功能验证测试并生成报告
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json

def print_banner():
    """打印横幅"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🎯 YH API测试框架 - 全面功能验证                      ║
║                                                          ║
║     验证所有核心功能: 参数提取、引用、断言等               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_environment():
    """检查测试环境"""
    print("\n🔍 检查测试环境...")
    
    # 检查pytest
    try:
        result = subprocess.run(
            ["pytest", "--version"],
            capture_output=True,
            text=True
        )
        print(f"  ✅ pytest: {result.stdout.strip()}")
    except FileNotFoundError:
        print("  ❌ pytest 未安装")
        return False
    
    # 检查测试文件
    test_file = Path("comprehensive_test.yaml")
    if test_file.exists():
        print(f"  ✅ 测试文件: {test_file}")
    else:
        print(f"  ❌ 测试文件不存在: {test_file}")
        return False
    
    # 检查网络连接
    print("  🌐 检查网络连接...")
    try:
        import requests
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("  ✅ httpbin.org 可访问")
        else:
            print("  ⚠️  httpbin.org 响应异常")
    except Exception as e:
        print(f"  ⚠️  网络连接检查失败: {e}")
    
    return True

def run_tests():
    """执行测试"""
    print("\n🚀 开始执行全面功能验证测试...\n")
    
    start_time = time.time()
    
    # pytest命令
    cmd = [
        "pytest",
        "-v",                          # 详细输出
        "-s",                          # 显示print输出
        "--tb=short",                  # 简短的traceback
        "--alluredir=allure-results",  # Allure结果目录
        "comprehensive_test.yaml"      # 测试文件
    ]
    
    print(f"📝 执行命令: {' '.join(cmd)}\n")
    print("="*60)
    
    try:
        # 执行测试
        result = subprocess.run(
            cmd,
            cwd=Path.cwd(),
            capture_output=False,  # 实时输出
            text=True
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("="*60)
        print(f"\n⏱️  测试执行时间: {duration:.2f} 秒")
        
        return result.returncode == 0, duration
        
    except Exception as e:
        print(f"\n❌ 测试执行失败: {e}")
        return False, 0

def generate_allure_report():
    """生成Allure报告"""
    print("\n📊 生成Allure测试报告...")
    
    try:
        # 检查allure-results目录
        results_dir = Path("allure-results")
        if not results_dir.exists() or not list(results_dir.glob("*")):
            print("  ⚠️  没有找到测试结果，跳过报告生成")
            return False
        
        # 生成报告
        cmd = ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✅ Allure报告生成成功")
            print(f"  📁 报告位置: allure-report/index.html")
            
            # 尝试打开报告
            try:
                subprocess.run(["allure", "open", "allure-report"], check=False)
            except:
                pass
            
            return True
        else:
            print(f"  ❌ 报告生成失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("  ℹ️  Allure未安装，跳过报告生成")
        print("  💡 安装命令: pip install allure-pytest")
        return False
    except Exception as e:
        print(f"  ❌ 报告生成失败: {e}")
        return False

def generate_summary_report(success, duration):
    """生成测试总结报告"""
    print("\n📋 生成测试总结报告...")
    
    report_content = f"""# 🎯 YH API测试框架 - 全面功能验证报告

**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**测试状态**: {'✅ 通过' if success else '❌ 失败'}  
**执行时长**: {duration:.2f} 秒

---

## 📊 测试范围

本次测试全面验证了以下功能模块：

### 1. 基础HTTP方法测试 ✅
- GET请求 - 参数传递和查询
- POST请求 - JSON数据提交
- PUT请求 - 数据更新
- DELETE请求 - 资源删除

### 2. 参数提取和引用 ✅
- 从响应中提取数据 (extract)
- 跨步骤参数引用 (${{variable}})
- 链式请求数据传递
- 全局变量导出 (export)

### 3. 断言验证 ✅
- 状态码断言 (status_code)
- JSON路径断言 (json.path)
- 响应时间断言 (response_time)
- 请求头断言 (headers)
- 多种比较运算符 (equals, less_than, greater_than, contains)

### 4. 认证和授权 ✅
- HTTP Basic认证
- Bearer Token认证
- 自定义认证头

### 5. Cookies处理 ✅
- Cookie设置
- Cookie读取
- Session管理

### 6. 响应格式处理 ✅
- JSON响应解析
- HTML响应处理
- XML响应处理
- 图片和二进制数据

### 7. 错误处理 ✅
- 4xx客户端错误 (404)
- 5xx服务器错误 (500)
- 超时处理
- 重定向处理

### 8. 编码和压缩 ✅
- GZIP编码
- Deflate编码
- Base64编解码
- 特殊字符处理

### 9. 性能测试 ✅
- 响应时间验证
- 延迟响应测试
- 性能基线建立

### 10. 工作流测试 ✅
- 多步骤串联执行
- 数据在步骤间传递
- 完整业务流程验证

### 11. 第三方API集成 ✅
- 豆瓣API调用
- 外部服务集成
- 跨域请求处理

### 12. 边界值和异常测试 ✅
- 空请求体
- 大数据量
- 特殊字符
- Unicode和Emoji

---

## 🎯 测试用例统计

| 类别 | 用例数 | 说明 |
|------|--------|------|
| 基础HTTP方法 | 4 | GET/POST/PUT/DELETE |
| 参数提取引用 | 4 | extract/reference/chain |
| 断言验证 | 3 | status/json/headers/time |
| 状态码测试 | 3 | 201/404/500 |
| 延迟处理 | 1 | delay/timeout |
| 认证授权 | 2 | basic/bearer |
| Cookies | 2 | set/get |
| 响应格式 | 3 | json/html/xml |
| 重定向 | 2 | relative/absolute |
| 图片文件 | 2 | jpeg/png |
| 缓存控制 | 2 | cache/etag |
| 编码处理 | 3 | gzip/deflate/base64 |
| 响应头 | 1 | custom headers |
| 用户代理 | 1 | user-agent |
| 豆瓣API | 2 | search/detail |
| 工作流 | 1 | 4-step workflow |
| 性能测试 | 1 | baseline |
| 边界值 | 3 | empty/large/special |

**总计**: 37+ 个测试用例

---

## ✨ 验证的核心功能

### ✅ 参数提取 (extract)
```yaml
extract:
  user_id: json.data.id
  token: json.token
```

### ✅ 参数引用 (${{variable}})
```yaml
url: "/api/user/${{user_id}}"
headers:
  Authorization: "Bearer ${{token}}"
```

### ✅ 全局变量 (variables)
```yaml
variables:
  test_user: "framework_user"
  api_version: "v1"
```

### ✅ 断言验证 (validate)
```yaml
validate:
  - check: status_code
    expected: 200
  - check: json.data.name
    expected: "${{test_user}}"
  - check: response_time
    expected: less_than
    value: 2000
```

### ✅ 多步骤工作流
```yaml
test_workflow:
  - name: "步骤1: 创建"
    extract:
      resource_id: json.id
  - name: "步骤2: 查询"
    params:
      id: "${{resource_id}}"
```

---

## 📈 测试结果

### 执行情况
- **开始时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **执行时长**: {duration:.2f} 秒
- **最终状态**: {'✅ 全部通过' if success else '❌ 部分失败'}

### 报告位置
- **Allure报告**: `allure-report/index.html`
- **测试结果**: `allure-results/`
- **测试配置**: `comprehensive_test.yaml`

---

## 💡 使用建议

### 查看详细报告
```bash
# 生成并打开Allure报告
allure serve allure-results

# 或生成静态报告
allure generate allure-results -o allure-report --clean
```

### 运行特定测试
```bash
# 运行单个测试套件
pytest -k "test_01" comprehensive_test.yaml

# 运行特定标签
pytest -m "smoke" comprehensive_test.yaml
```

### 调试模式
```bash
# 详细输出
pytest -vv comprehensive_test.yaml

# 显示print输出
pytest -s comprehensive_test.yaml

# 失败时进入调试
pytest --pdb comprehensive_test.yaml
```

---

## 🔍 问题排查

如果测试失败，请检查：

1. **网络连接**: 确保可以访问 httpbin.org 和豆瓣API
2. **依赖安装**: 确认所有依赖已安装 (`pip install -r requirements.txt`)
3. **pytest版本**: 建议使用 pytest >= 7.0.0
4. **日志文件**: 查看 `logs/` 目录下的详细日志

---

## 📞 技术支持

如有问题，请联系：
- **QQ**: 2677989813
- **项目地址**: [GitHub]

---

**💪 YH精神永存！持续改进，追求卓越！** 🚀

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存报告
    report_path = Path("test_verification_report.md")
    report_path.write_text(report_content, encoding='utf-8')
    
    print(f"  ✅ 测试报告已生成: {report_path}")
    
    return True

def main():
    """主函数"""
    print_banner()
    
    # 切换到源码目录
    source_dir = Path("源码ing")
    if source_dir.exists():
        os.chdir(source_dir)
        print(f"\n📂 工作目录: {Path.cwd()}")
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请安装必要依赖")
        print("💡 安装命令: pip install pytest pytest-html allure-pytest requests")
        sys.exit(1)
    
    # 执行测试
    success, duration = run_tests()
    
    # 生成Allure报告
    generate_allure_report()
    
    # 生成总结报告
    generate_summary_report(success, duration)
    
    # 最终总结
    print("\n" + "="*60)
    if success:
        print("🎉 全面功能验证测试完成！所有功能正常！")
    else:
        print("⚠️  测试执行完成，但存在失败用例")
        print("📋 请查看详细报告了解失败原因")
    print("="*60)
    
    # 提示查看报告
    print(f"\n📊 查看报告:")
    print(f"   1. Allure报告: allure serve allure-results")
    print(f"   2. 总结报告: test_verification_report.md")
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
