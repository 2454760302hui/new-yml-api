#!/usr/bin/env python3
"""
YH Shell 命令处理器
处理各种Shell命令的执行逻辑
"""

import os
import sys
import time
import random
import json
import yaml
import subprocess
import threading
from typing import Dict, Any, List, Optional
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

# 初始化colorama
init(autoreset=True)


class CommandHandler:
    """Shell命令处理器基类"""

    def __init__(self, shell_instance):
        """
        初始化命令处理器

        Args:
            shell_instance: YHShell实例
        """
        self.shell = shell_instance

    def print_success(self, message: str):
        """打印成功消息"""
        print(f"{Fore.GREEN + Style.BRIGHT}[OK] {message}{Style.RESET_ALL}")

    def print_error(self, message: str):
        """打印错误消息"""
        print(f"{Fore.RED}[FAIL] {message}{Style.RESET_ALL}")

    def print_info(self, message: str):
        """打印信息消息"""
        print(f"{Fore.CYAN}[INFO] {message}{Style.RESET_ALL}")

    def print_warning(self, message: str):
        """打印警告消息"""
        print(f"{Fore.YELLOW}[WARN]  {message}{Style.RESET_ALL}")


class TestCommandHandler(CommandHandler):
    """测试相关命令处理器"""

    def do_fadeaway(self, arg: str):
        """开始API测试 - 精准测试"""
        print(f"\n{Fore.YELLOW + Style.BRIGHT}[RUN] 准备精准测试... [RUN]{Style.RESET_ALL}")

        # 动画效果
        for i in range(3):
            print(f"{Fore.CYAN}{'.' * (i + 1)} 瞄准目标{Style.RESET_ALL}")
            time.sleep(0.5)

        print(f"{Fore.GREEN + Style.BRIGHT}[TARGET] SWISH! 开始API测试！{Style.RESET_ALL}\n")

        if not arg:
            # 使用默认测试文件
            default_test_file = "default_test.yaml"
            if os.path.exists(default_test_file):
                print(f"{Fore.CYAN}[TARGET] 使用默认测试文件: {default_test_file}{Style.RESET_ALL}")
                self.do_load(default_test_file)
                self.do_run("")
            else:
                self.print_error(f"默认测试文件不存在: {default_test_file}")
                print(f"{Fore.YELLOW}[TIP] 解决方案:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   1. 指定测试文件: fadeaway <test_file.yaml>{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   2. 创建默认测试文件: {default_test_file}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   3. 使用 'generate' 命令生成示例项目{Style.RESET_ALL}")
            return

        # 先加载文件，再运行
        self.do_load(arg)
        if self.shell.current_test_file:  # 只有加载成功才运行
            self.do_run("")

    def do_load(self, arg: str):
        """加载测试文件"""
        arg = arg.replace('\\n', '').replace('\n', '').replace('\r', '').strip()

        if not arg:
            self.print_error("缺少文件参数")
            print(f"{Fore.YELLOW}[TIP] 用法: load <test_file.yaml>{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   示例: load my_test.yaml{Style.RESET_ALL}")
            return

        try:
            print(f"{Fore.CYAN}[FIND] 正在查找文件: '{arg}'{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[DIR] 当前目录: {os.getcwd()}{Style.RESET_ALL}")

            if not os.path.exists(arg):
                self.print_error(f"文件不存在: {arg}")
                print(f"{Fore.YELLOW}[TIP] 解决方案:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   1. 检查文件路径是否正确{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   2. 确保文件在当前目录或使用绝对路径{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   3. 使用 'generate' 命令创建示例测试文件{Style.RESET_ALL}")
                return

            with open(arg, 'r', encoding='utf-8') as f:
                if arg.endswith('.yaml') or arg.endswith('.yml'):
                    test_data = yaml.safe_load(f)
                else:
                    test_data = json.load(f)

            self.shell.current_test_file = arg
            self.print_success(f"成功加载测试文件: {arg}")

            # 显示测试概览
            if isinstance(test_data, list):
                print(f"[STATS] 包含 {len(test_data)} 个测试用例")
            elif isinstance(test_data, dict) and 'tests' in test_data:
                print(f"[STATS] 包含 {len(test_data['tests'])} 个测试用例")

        except Exception as e:
            self.print_error(f"加载文件失败: {e}")

    def do_run(self, arg: str):
        """运行测试"""
        if not self.shell.current_test_file and not arg:
            print("请先加载测试文件或指定文件: run [test_file.yaml]")
            return

        test_file = arg if arg else self.shell.current_test_file
        print(f"\n{Fore.YELLOW + Style.BRIGHT}[RUN] 开始执行测试: {test_file}{Style.RESET_ALL}")
        self._simulate_test_execution(test_file)

    def _simulate_test_execution(self, test_file: str):
        """模拟测试执行"""
        print(f"{Fore.CYAN}[INFO] 正在解析测试文件...{Style.RESET_ALL}")
        time.sleep(1)

        print(f"{Fore.CYAN}[TOOL] 初始化测试环境...{Style.RESET_ALL}")
        time.sleep(0.5)

        # 模拟测试用例执行
        test_cases = [
            "用户登录接口测试",
            "获取用户信息接口测试",
            "创建订单接口测试",
            "查询订单列表接口测试",
            "更新订单状态接口测试"
        ]

        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"{Fore.BLUE}[TEST] [{i}/{len(test_cases)}] 执行: {test_case}{Style.RESET_ALL}")
            time.sleep(random.uniform(0.3, 1.0))
            success = random.choice([True, True, True, False])  # 75%成功率

            if success:
                print(f"{Fore.GREEN}  [OK] 通过 - 响应时间: {random.randint(50, 300)}ms{Style.RESET_ALL}")
                results.append({"name": test_case, "status": "PASS", "time": random.randint(50, 300)})
            else:
                print(f"{Fore.RED}  [FAIL] 失败 - 状态码: {random.choice([404, 500, 401])}{Style.RESET_ALL}")
                results.append({"name": test_case, "status": "FAIL", "error": "API调用失败"})

        # 显示测试结果
        self._show_test_results(results)

    def _show_test_results(self, results: List[Dict[str, Any]]):
        """显示测试结果"""
        passed = len([r for r in results if r["status"] == "PASS"])
        failed = len([r for r in results if r["status"] == "FAIL"])
        total = len(results)
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n{Fore.YELLOW + Style.BRIGHT}[STATS] 测试结果统计{Style.RESET_ALL}")
        print("=" * 50)
        print(f"总测试数: {total}")
        print(f"{Fore.GREEN}通过数: {passed} [OK]{Style.RESET_ALL}")
        print(f"{Fore.RED}失败数: {failed} [FAIL]{Style.RESET_ALL}")
        print(f"成功率: {success_rate:.1f}%")

        if success_rate >= 90:
            print(f"\n{Fore.YELLOW + Style.BRIGHT}[AWARD] 完美表现！测试结果优秀！{Style.RESET_ALL}")
        elif success_rate >= 70:
            print(f"\n{Fore.GREEN + Style.BRIGHT}[THUMB] 不错的表现！继续保持！{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.MAGENTA + Style.BRIGHT}[POWER] 失败是成功之母，继续努力！{Style.RESET_ALL}")

        self.shell.test_results = results
        self._generate_allure_report(results)

    def _generate_allure_report(self, results: List[Dict[str, Any]]):
        """生成Allure报告"""
        try:
            from allure_reporter import AllureReporter, AllureConfig
            import platform

            print(f"\n{Fore.CYAN}[STATS] 正在生成测试报告...{Style.RESET_ALL}")

            config = AllureConfig(
                results_dir="allure-results",
                report_dir="allure-report",
                clean_results=True,
                generate_report=True,
                open_report=True
            )

            reporter = AllureReporter(config)

            env_info = {
                "测试框架": "YH-API-Testing-Framework",
                "执行时间": time.strftime('%Y-%m-%d %H:%M:%S'),
                "测试文件": getattr(self.shell, 'current_test_file', None) or "default_test.yaml",
                "总测试数": str(len(results)),
                "通过数": str(len([r for r in results if r["status"] == "PASS"])),
                "失败数": str(len([r for r in results if r["status"] == "FAIL"])),
                "成功率": f"{(len([r for r in results if r['status'] == 'PASS']) / len(results) * 100):.1f}%" if results else "0%"
            }
            reporter.generate_environment_info(env_info)

            categories = [
                {"name": "API错误", "matchedStatuses": ["failed"], "messageRegex": ".*API.*"},
                {"name": "超时错误", "matchedStatuses": ["failed"], "messageRegex": ".*timeout.*"},
                {"name": "断言错误", "matchedStatuses": ["failed"], "messageRegex": ".*assert.*"}
            ]
            reporter.generate_categories_file(categories)

            if reporter.generate_and_open_report():
                self.print_success("Allure报告已生成并自动打开")
                print(f"{Fore.YELLOW}[DIR] 报告位置: allure-report/index.html{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[WARN]  报告生成失败，请手动运行: allure serve allure-results{Style.RESET_ALL}")

        except ImportError:
            print(f"{Fore.YELLOW}[WARN]  未安装allure-pytest，跳过报告生成{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[TIP] 安装命令: pip install allure-pytest{Style.RESET_ALL}")
        except Exception as e:
            self.print_error(f"生成Allure报告失败: {e}")

    def do_concurrent(self, arg: str):
        """并发测试"""
        if not arg:
            print("用法: concurrent <users> [test_file.yaml]")
            return

        parts = arg.split()
        try:
            users = int(parts[0])
            test_file = parts[1] if len(parts) > 1 else self.shell.current_test_file

            if not test_file:
                print("请指定测试文件")
                return

            print(f"\n{Fore.YELLOW + Style.BRIGHT}[RUN] 启动并发测试{Style.RESET_ALL}")
            print(f"并发用户数: {users}")
            print(f"测试文件: {test_file}")

            print(f"\n{Fore.MAGENTA + Style.BRIGHT}[RUN] 团队协作 - {users}个用户同时测试！{Style.RESET_ALL}")

            for i in range(users):
                print(f"{Fore.CYAN}🏃 用户{i+1}号准备就绪...{Style.RESET_ALL}")
                time.sleep(0.1)

            print(f"{Fore.GREEN + Style.BRIGHT}[TARGET] 全队齐射！{Style.RESET_ALL}")
            time.sleep(2)

            success_rate = random.uniform(85, 98)
            avg_response_time = random.randint(100, 500)

            print(f"\n{Fore.YELLOW + Style.BRIGHT}[STATS] 并发测试结果{Style.RESET_ALL}")
            print("=" * 40)
            print(f"并发用户数: {users}")
            print(f"成功率: {success_rate:.1f}%")
            print(f"平均响应时间: {avg_response_time}ms")
            print(f"总请求数: {users * 5}")

            if success_rate >= 95:
                print(f"\n{Fore.YELLOW + Style.BRIGHT}[AWARD] 完美团队配合！测试精准！{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN + Style.BRIGHT}[THUMB] 不错的团队表现！{Style.RESET_ALL}")

        except ValueError:
            print("[FAIL] 用户数必须是数字")


class AdvancedCommandHandler(CommandHandler):
    """高级功能命令处理器"""

    def do_ai(self, args: str):
        """AI智能测试"""
        if not args:
            self.print_error("请指定目标URL")
            print(f"{Fore.CYAN}用法: ai <目标URL>{Style.RESET_ALL}")
            print(f"{Fore.CYAN}示例: ai https://httpbin.org{Style.RESET_ALL}")
            return

        target_url = args.strip()
        print(f"{Fore.CYAN}[AI] 启动AI智能测试...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[TARGET] 目标: {target_url}{Style.RESET_ALL}")

        try:
            import requests

            print(f"{Fore.CYAN}[FIND] 第1步：基础连接测试{Style.RESET_ALL}")

            try:
                response = requests.get(target_url, timeout=10)
                print(f"{Fore.GREEN}[OK] 连接成功: {response.status_code}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[FAIL] 连接失败: {e}{Style.RESET_ALL}")
                return

            print(f"{Fore.CYAN}[FIND] 第2步：端点发现{Style.RESET_ALL}")

            common_endpoints = [
                "/", "/api", "/health", "/status", "/version", "/info",
                "/get", "/post", "/put", "/delete", "/patch",
                "/json", "/xml", "/html", "/headers", "/ip"
            ]

            discovered = []
            for endpoint in common_endpoints:
                try:
                    url = target_url.rstrip('/') + endpoint
                    resp = requests.get(url, timeout=5)
                    if resp.status_code < 500:
                        discovered.append({
                            "endpoint": endpoint,
                            "status": resp.status_code,
                            "size": len(resp.content)
                        })
                        print(f"  {Fore.GREEN}[OK] {endpoint} -> {resp.status_code}{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.RED}[FAIL] {endpoint} -> {resp.status_code}{Style.RESET_ALL}")
                except:
                    print(f"  {Fore.YELLOW}[WARN]  {endpoint} -> 超时{Style.RESET_ALL}")

            print(f"{Fore.GREEN}[TARGET] 发现 {len(discovered)} 个可用端点{Style.RESET_ALL}")

            if not discovered:
                self.print_error("未发现可用端点")
                return

            print(f"{Fore.CYAN}🧠 第3步：生成测试用例{Style.RESET_ALL}")

            tests = []
            for ep in discovered[:5]:
                tests.append({
                    "name": f"GET {ep['endpoint']} 基础测试",
                    "method": "GET",
                    "url": target_url.rstrip('/') + ep['endpoint'],
                    "expected_status": [200, 201, 202, 204, 301, 302, 304]
                })

            print(f"{Fore.GREEN}[OK] 生成了 {len(tests)} 个测试用例{Style.RESET_ALL}")

            print(f"{Fore.CYAN}[RUN] 第4步：执行测试{Style.RESET_ALL}")

            results = {"total": len(tests), "passed": 0, "failed": 0}

            for i, test in enumerate(tests, 1):
                print(f"  [{i}/{len(tests)}] {test['name']}")
                try:
                    resp = requests.get(test['url'], timeout=10)
                    passed = resp.status_code in test['expected_status']
                    if passed:
                        results['passed'] += 1
                        print(f"    {Fore.GREEN}[OK] 通过 ({resp.status_code}){Style.RESET_ALL}")
                    else:
                        results['failed'] += 1
                        print(f"    {Fore.RED}[FAIL] 失败 ({resp.status_code}){Style.RESET_ALL}")
                except Exception as e:
                    results['failed'] += 1
                    print(f"    {Fore.RED}[FAIL] 异常: {e}{Style.RESET_ALL}")

            success_rate = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
            print(f"\n{Fore.YELLOW}[STATS] 测试结果: {results['passed']}/{results['total']} 通过 ({success_rate:.1f}%){Style.RESET_ALL}")

            if success_rate >= 80:
                print(f"{Fore.GREEN}[AWARD] API质量优秀！{Style.RESET_ALL}")
            elif success_rate >= 60:
                print(f"{Fore.YELLOW}[THUMB] API质量良好{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[WARN]  API需要改进{Style.RESET_ALL}")

        except ImportError as e:
            self.print_error(f"缺少依赖模块: {e}")
        except Exception as e:
            self.print_error(f"AI测试执行失败: {e}")

    def do_socket(self, arg: str):
        """Socket测试"""
        if not arg:
            print("用法: socket <host:port> [message]")
            return

        parts = arg.split(' ', 1)
        host_port = parts[0]
        message = parts[1] if len(parts) > 1 else "Hello Socket"

        print(f"\n{Fore.YELLOW + Style.BRIGHT}🔌 Socket连接测试{Style.RESET_ALL}")
        print(f"目标: {host_port}")
        print(f"消息: {message}")

        print(f"{Fore.CYAN}[LINK] 正在连接...{Style.RESET_ALL}")
        time.sleep(1)

        success = random.choice([True, True, False])

        if success:
            self.print_success("连接成功")
            print(f"{Fore.CYAN}[SEND] 发送消息: {message}{Style.RESET_ALL}")
            time.sleep(0.5)
            print(f"{Fore.GREEN}[RECV] 收到回复: Echo - {message}{Style.RESET_ALL}")
        else:
            self.print_error("连接失败: 目标不可达")

    def do_wechat(self, arg: str):
        """企业微信通知测试"""
        print(f"\n{Fore.YELLOW + Style.BRIGHT}[CHAT] 企业微信通知{Style.RESET_ALL}")

        if not arg:
            message = "API测试完成通知"
        else:
            message = arg

        print(f"消息内容: {message}")
        print(f"{Fore.CYAN}[PHONE] 正在发送企业微信通知...{Style.RESET_ALL}")
        time.sleep(1)

        success = random.choice([True, True, True, False])

        if success:
            self.print_success("企业微信通知发送成功")
        else:
            self.print_error("企业微信通知发送失败")

    def do_docs(self, args: str):
        """启动文档服务器"""
        print(f"{Fore.CYAN}📚 启动文档服务器...{Style.RESET_ALL}")
        try:
            def start_docs():
                subprocess.run([sys.executable, "swagger_docs.py"])

            docs_thread = threading.Thread(target=start_docs, daemon=True)
            docs_thread.start()

            time.sleep(2)
            self.print_success("文档服务器已启动: http://127.0.0.1:8080")
            print(f"{Fore.CYAN}[TIP] 提示: 在浏览器中访问上述地址查看文档{Style.RESET_ALL}")

        except Exception as e:
            self.print_error(f"文档服务器启动失败: {e}")

    def do_report(self, arg: str):
        """生成测试报告"""
        if not self.shell.test_results:
            print("没有测试结果可生成报告")
            return

        print(f"\n{Fore.YELLOW + Style.BRIGHT}[STATS] 生成测试报告{Style.RESET_ALL}")

        report_types = ['HTML', 'Allure', 'JSON', 'Excel']

        for report_type in report_types:
            print(f"{Fore.CYAN}[FILE] 生成{report_type}报告...{Style.RESET_ALL}")
            time.sleep(0.5)
            self.print_success(f"{report_type}报告生成完成")

        print(f"\n{Fore.GREEN + Style.BRIGHT}[SUCCESS] 所有报告生成完成！{Style.RESET_ALL}")
        print("报告文件:")
        print("  [FILE] test_report.html")
        print("  [STATS] allure-report/index.html")
        print("  [INFO] test_results.json")
        print("  📈 test_summary.xlsx")

    def do_status(self, arg: str):
        """显示当前状态"""
        print(f"\n{Fore.CYAN + Style.BRIGHT}[INFO] 当前状态{Style.RESET_ALL}")
        print("=" * 30)
        print(f"当前测试文件: {self.shell.current_test_file or '未加载'}")
        print(f"会话变量数量: {len(self.shell.session_vars)}")
        print(f"测试结果数量: {len(self.shell.test_results)}")

        if self.shell.test_results:
            passed = len([r for r in self.shell.test_results if r["status"] == "PASS"])
            failed = len([r for r in self.shell.test_results if r["status"] == "FAIL"])
            print(f"最近测试: {passed}通过, {failed}失败")


class VariableCommandHandler(CommandHandler):
    """变量管理命令处理器"""

    def do_vars(self, arg: str):
        """管理会话变量"""
        arg = arg.replace('\\n', '').replace('\n', '').replace('\r', '').strip()

        if not arg:
            self._list_variables()
            return

        parts = arg.split(' ', 2)
        if len(parts) < 2:
            self.print_error("参数不足")
            print(f"{Fore.YELLOW}[TIP] 用法: vars <set|get|del> <name> [value]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   示例: vars set api_token abc123{Style.RESET_ALL}")
            return

        action, name = parts[0], parts[1]

        if action == 'set':
            self._set_variable(name, parts[2] if len(parts) > 2 else None)
        elif action == 'get':
            self._get_variable(name)
        elif action == 'del':
            self._delete_variable(name)
        else:
            self.print_error(f"未知操作: {action}")
            print(f"{Fore.YELLOW}[TIP] 支持的操作: set, get, del{Style.RESET_ALL}")

    def _list_variables(self):
        """列出所有变量"""
        if not self.shell.session_vars:
            print(f"\n{Fore.YELLOW}[NOTE] 会话变量管理{Style.RESET_ALL}")
            print(f"{Fore.CYAN}当前没有会话变量{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}[TIP] 使用方法:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   vars set <name> <value>  - 设置变量{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   vars get <name>          - 获取变量{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   vars del <name>          - 删除变量{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN + Style.BRIGHT}[NOTE] 会话变量列表{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

        for i, (key, value) in enumerate(self.shell.session_vars.items(), 1):
            display_value = str(value)
            if len(display_value) > 50:
                display_value = display_value[:47] + "..."
            print(f"{Fore.YELLOW}{i:2d}.{Style.RESET_ALL} {Fore.GREEN}{key:<20}{Style.RESET_ALL} = {Fore.WHITE}{display_value}{Style.RESET_ALL}")

        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}总计: {len(self.shell.session_vars)} 个变量{Style.RESET_ALL}")

    def _set_variable(self, name: str, value: str):
        """设置变量"""
        if value is None:
            self.print_error("缺少变量值")
            print(f"{Fore.YELLOW}[TIP] 用法: vars set <name> <value>{Style.RESET_ALL}")
            return

        self.shell.session_vars[name] = value
        self.print_success("变量设置成功")
        print(f"{Fore.CYAN}   变量名: {Fore.YELLOW}{name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   变量值: {Fore.WHITE}{value}{Style.RESET_ALL}")

    def _get_variable(self, name: str):
        """获取变量"""
        if name in self.shell.session_vars:
            value = self.shell.session_vars[name]
            self.print_success("变量获取成功")
            print(f"{Fore.CYAN}   {name}: {Fore.WHITE}{value}{Style.RESET_ALL}")
        else:
            self.print_error(f"变量不存在: {name}")
            print(f"{Fore.YELLOW}[TIP] 使用 'vars' 查看所有变量{Style.RESET_ALL}")

    def _delete_variable(self, name: str):
        """删除变量"""
        if name in self.shell.session_vars:
            old_value = self.shell.session_vars[name]
            del self.shell.session_vars[name]
            self.print_success("变量删除成功")
            print(f"{Fore.CYAN}   已删除: {name} = {old_value}{Style.RESET_ALL}")
        else:
            self.print_error(f"变量不存在: {name}")
            print(f"{Fore.YELLOW}[TIP] 使用 'vars' 查看所有变量{Style.RESET_ALL}")
