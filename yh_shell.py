#!/usr/bin/env python3
"""
YH风格的Shell启动界面
API测试框架交互式命令行界面

重构说明：
- 拆分为多个模块，提高可维护性
- 使用命令处理器模式
- 项目生成器独立模块
"""

import os
import sys
import random
from typing import Dict, Any, List, Optional
import cmd
from colorama import init, Fore, Style

# 导入模块化组件
try:
    from shell.commands import TestCommandHandler, AdvancedCommandHandler, VariableCommandHandler
    from shell.project_generator import ProjectGenerator
except ImportError:
    # 支持直接运行
    import importlib.util
    spec = importlib.util.spec_from_file_location("commands", os.path.join(os.path.dirname(__file__), "shell", "commands.py"))
    commands_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(commands_module)
    TestCommandHandler = commands_module.TestCommandHandler
    AdvancedCommandHandler = commands_module.AdvancedCommandHandler
    VariableCommandHandler = commands_module.VariableCommandHandler

    spec2 = importlib.util.spec_from_file_location("project_generator", os.path.join(os.path.dirname(__file__), "shell", "project_generator.py"))
    generator_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(generator_module)
    ProjectGenerator = generator_module.ProjectGenerator

# 初始化colorama
init(autoreset=True)


class YHShell(cmd.Cmd):
    """YH风格的API测试框架Shell - 重构版"""

    def __init__(self):
        super().__init__()
        self.intro = self._get_yh_intro()
        self.prompt = f"{Fore.YELLOW + Style.BRIGHT}🚀 YH-API-Test{Fore.CYAN} >{Style.RESET_ALL} "
        self.current_test_file: Optional[str] = None
        self.test_results: List[Dict[str, Any]] = []
        self.session_vars: Dict[str, Any] = {}
        self.command_count: int = 0

        # 初始化命令处理器
        self.test_handler = TestCommandHandler(self)
        self.advanced_handler = AdvancedCommandHandler(self)
        self.variable_handler = VariableCommandHandler(self)
        self.project_generator = ProjectGenerator()

    def _get_yh_intro(self) -> str:
        """获取YH风格的启动界面"""
        return """
{yellow}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    🚀 API Testing                                             ║
    ║    ⚡ 智能 • 高效 • 专业                                        ║
    ║                                                               ║
    ║    🔧 HTTP/Socket  📊 Reports  🤖 AI Testing                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝



{cyan}
    🏆 框架特性:
    • 🎯 精准的API测试 - 智能高效，追求完美
    • 🔥 并发测试支持 - 高性能，永不放弃
    • 📊 详细的测试报告 - 数据驱动，追求完美
    • 🚀 Socket/WebSocket测试 - 全方位覆盖
    • 💬 企业微信通知 - 团队协作无缝对接
    • 🎨 Allure报告 - 专业级测试展示
{reset}

{green}
    输入 'help' 查看所有命令
    输入 'inspire' 获取激励语录
    输入 'fadeaway' 开始你的API测试之旅

    📞 技术支持 QQ: 2677989813
{reset}
        """.format(
            yellow=Fore.YELLOW + Style.BRIGHT,
            cyan=Fore.CYAN + Style.BRIGHT,
            green=Fore.GREEN + Style.BRIGHT,
            reset=Style.RESET_ALL
        )

    # ========== 测试相关命令 ==========
    def do_fadeaway(self, arg: str):
        """开始API测试 - 精准测试"""
        self.test_handler.do_fadeaway(arg)

    def do_load(self, arg: str):
        """加载测试文件"""
        self.test_handler.do_load(arg)

    def do_run(self, arg: str):
        """运行测试"""
        self.test_handler.do_run(arg)

    def do_concurrent(self, arg: str):
        """并发测试"""
        self.test_handler.do_concurrent(arg)

    # ========== 高级功能命令 ==========
    def do_ai(self, arg: str):
        """AI智能测试"""
        self.advanced_handler.do_ai(arg)

    def do_socket(self, arg: str):
        """Socket测试"""
        self.advanced_handler.do_socket(arg)

    def do_wechat(self, arg: str):
        """企业微信通知测试"""
        self.advanced_handler.do_wechat(arg)

    def do_docs(self, arg: str):
        """启动文档服务器"""
        self.advanced_handler.do_docs(arg)

    def do_report(self, arg: str):
        """生成测试报告"""
        self.advanced_handler.do_report(arg)

    def do_status(self, arg: str):
        """显示当前状态"""
        self.advanced_handler.do_status(arg)

    # ========== 变量管理命令 ==========
    def do_vars(self, arg: str):
        """管理会话变量"""
        self.variable_handler.do_vars(arg)

    # ========== 项目生成命令 ==========
    def do_generate(self, arg: str):
        """生成测试项目"""
        arg = arg.replace('\\n', '').replace('\n', '').replace('\r', '').strip()
        project_name = arg if arg else "api_test_project"

        print(f"{Fore.YELLOW + Style.BRIGHT}📦 生成测试项目...{Style.RESET_ALL}")

        try:
            self.project_generator.generate_test_project(project_name)
            print(f"{Fore.GREEN + Style.BRIGHT}🎉 测试项目生成成功！{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📁 项目目录: {project_name}/{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 使用说明:{Style.RESET_ALL}")
            print(f"  1. 进入项目目录: cd {project_name}")
            print(f"  2. 修改配置文件: config/test_config.yaml")
            print(f"  3. 更新测试用例: tests/api_tests.yaml")
            print(f"  4. 运行测试: python run.py")

        except Exception as e:
            print(f"{Fore.RED}❌ 项目生成失败: {e}{Style.RESET_ALL}")

    # ========== 其他命令 ==========
    def do_inspire(self, arg: str):
        """显示激励语录"""
        quotes = [
            "🚀 持续改进，追求卓越。",
            "💡 创新思维，突破极限。",
            "⚡ 勇于尝试，不惧失败。",
            "🎯 专注于过程，结果自然会来。",
            "💪 伟大来自于对细节的关注。",
            "🔥 要么全力以赴，要么回家。",
            "🏆 成功是在没有人看见的时候努力出来的。",
            "⭐ 宁愿尝试失败，也不愿不去尝试。",
            "🚀 困难是暂时的，但放弃是永远的。",
            "💎 压力造就钻石。"
        ]

        quote = random.choice(quotes)
        print(f"\n{Fore.YELLOW + Style.BRIGHT}🌟 YH激励语录 🌟{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA + Style.BRIGHT}{quote}{Style.RESET_ALL}\n")

    def do_quickstart(self, arg: str):
        """一键启动功能"""
        print(f"{Fore.CYAN}🚀 一键启动功能...{Style.RESET_ALL}")
        try:
            import subprocess
            subprocess.run([sys.executable, "quick_start.py"])
        except Exception as e:
            print(f"{Fore.RED}❌ 启动失败: {e}{Style.RESET_ALL}")

    def do_clear(self, arg: str):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self._get_yh_intro())

    def do_exit(self, arg: str):
        """退出程序"""
        print(f"\n{Fore.YELLOW + Style.BRIGHT}🌟 YH精神永存！{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA + Style.BRIGHT}感谢使用API测试框架，继续追求完美！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}\"持续改进，追求卓越！\" - YH{Style.RESET_ALL}\n")
        return True

    def do_quit(self, arg: str):
        """退出程序"""
        return self.do_exit(arg)

    def help_general(self):
        """显示通用帮助"""
        help_text = f"""
{Fore.YELLOW + Style.BRIGHT}🚀 YH API测试框架 - 命令帮助{Style.RESET_ALL}

{Fore.CYAN + Style.BRIGHT}📋 基础命令:{Style.RESET_ALL}
  inspire            - 显示激励语录
  fadeaway <file>    - 开始API测试（精准测试）
  load <file>        - 加载测试文件
  run [file]         - 运行测试
  status             - 显示当前状态
  clear              - 清屏并显示启动界面

{Fore.GREEN + Style.BRIGHT}🔧 测试管理:{Style.RESET_ALL}
  vars               - 管理会话变量
  vars set <k> <v>   - 设置变量
  vars get <k>       - 获取变量
  vars del <k>       - 删除变量

{Fore.MAGENTA + Style.BRIGHT}🚀 高级功能:{Style.RESET_ALL}
  concurrent <n> [f] - 并发测试（n个用户）
  socket <host:port> - Socket连接测试
  wechat [msg]       - 企业微信通知测试
  report             - 生成测试报告

{Fore.BLUE + Style.BRIGHT}🤖 AI智能功能:{Style.RESET_ALL}
  ai <url>           - AI智能测试（自动生成和执行测试用例）
  quickstart         - 一键启动所有功能
  docs               - 启动文档服务器

{Fore.GREEN + Style.BRIGHT}📦 项目生成:{Style.RESET_ALL}
  generate [name]    - 生成完整的测试项目目录

{Fore.RED + Style.BRIGHT}🚪 退出:{Style.RESET_ALL}
  exit / quit        - 退出程序

{Fore.MAGENTA + Style.BRIGHT}📞 联系支持:{Style.RESET_ALL}
  QQ: 2677989813     - 技术支持与交流

{Fore.YELLOW}💡 提示: 输入命令名称可查看详细帮助{Style.RESET_ALL}
{Fore.GREEN}🎯 快速开始: 输入 'fadeaway' 开始API测试之旅{Style.RESET_ALL}
        """
        print(help_text)

    def do_shell(self, args: str):
        """执行shell命令模式的API测试命令"""
        if not args:
            print(f"\n{Fore.CYAN + Style.BRIGHT}🐚 YH Shell命令模式{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW + Style.BRIGHT}📋 可用命令列表:{Style.RESET_ALL}\n")

            commands = [
                ("🚀 测试执行", [
                    ("run <file>", "运行测试文件"),
                    ("load <file>", "加载测试文件"),
                    ("fadeaway [file]", "执行精准测试"),
                    ("concurrent <n>", "并发测试")
                ]),
                ("🤖 智能功能", [
                    ("ai <url>", "AI智能测试"),
                    ("socket <host>", "Socket连接测试"),
                    ("wechat [msg]", "企业微信通知")
                ]),
                ("📊 报告管理", [
                    ("report", "生成测试报告"),
                    ("status", "查看当前状态"),
                    ("docs", "启动文档服务器")
                ]),
                ("🔧 工具功能", [
                    ("vars <op>", "变量管理"),
                    ("generate [name]", "生成测试项目"),
                    ("inspire", "获取激励语录")
                ])
            ]

            for category, cmd_list in commands:
                print(f"{Fore.MAGENTA + Style.BRIGHT}{category}:{Style.RESET_ALL}")
                for cmd, desc in cmd_list:
                    print(f"  {Fore.GREEN}shell {cmd:<15}{Style.RESET_ALL} - {Fore.WHITE}{desc}{Style.RESET_ALL}")
                print()

            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 示例: shell run my_test.yaml{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 提示: 所有shell命令都支持完整的参数传递{Style.RESET_ALL}")
            return

        clean_args = args.replace('\\n', '').replace('\n', '').replace('\r', '').strip()
        parts = clean_args.split()
        if not parts:
            return

        cmd = parts[0]
        cmd_args = " ".join(parts[1:]) if len(parts) > 1 else ""

        shell_commands = {
            'run': self.do_run,
            'load': self.do_load,
            'fadeaway': self.do_fadeaway,
            'concurrent': self.do_concurrent,
            'ai': self.do_ai,
            'report': self.do_report,
            'status': self.do_status,
            'docs': self.do_docs,
            'inspire': self.do_inspire,
            'socket': self.do_socket,
            'wechat': self.do_wechat,
            'vars': self.do_vars,
            'generate': self.do_generate
        }

        if cmd in shell_commands:
            print(f"\n{Fore.CYAN + Style.BRIGHT}🐚 YH Shell 执行中...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}┌─ 命令: {Fore.GREEN}{cmd}{Style.RESET_ALL}")
            if cmd_args:
                print(f"{Fore.YELLOW}├─ 参数: {Fore.WHITE}{cmd_args}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}└─ 状态: {Fore.GREEN}正在执行...{Style.RESET_ALL}\n")

            try:
                shell_commands[cmd](cmd_args)
                print(f"\n{Fore.GREEN}✅ Shell命令执行完成{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}❌ Shell命令执行失败: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ 不支持的shell命令: '{cmd}'{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 可用命令提示:{Style.RESET_ALL}")
            available_cmds = ['run', 'load', 'fadeaway', 'concurrent', 'ai', 'report', 'status', 'docs', 'inspire', 'socket', 'wechat', 'vars', 'generate']
            suggestions = [c for c in available_cmds if cmd.lower() in c.lower() or c.lower() in cmd.lower()]

            if suggestions:
                print(f"{Fore.GREEN}   🎯 推荐命令: {', '.join(suggestions)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}   📋 输入 'shell' 查看所有支持的命令{Style.RESET_ALL}")

    def default(self, line: str):
        """处理未知命令"""
        clean_line = line.replace('\\n', '').replace('\n', '').replace('\r', '').strip()

        if clean_line == "2":
            self.do_docs("")
            return
        elif clean_line == "6":
            print(f"{Fore.CYAN}🎯 执行数字命令6 - 生成测试项目{Style.RESET_ALL}")
            self.do_generate("")
            return

        command = line.strip()
        print(f"{Fore.RED}❌ 未知命令: '{command}'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 提示: 您可能想要使用以下命令之一:{Style.RESET_ALL}")

        available_commands = ['help', 'load', 'run', 'test', 'docs', 'vars', 'generate', 'inspire', 'fadeaway', 'exit']
        suggestions = []

        for cmd in available_commands:
            if command.lower() in cmd.lower() or cmd.lower() in command.lower():
                suggestions.append(cmd)

        if suggestions:
            print(f"{Fore.GREEN}   🎯 推荐命令: {', '.join(suggestions)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}   📋 输入 'help' 查看所有可用命令{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   🚀 输入 'fadeaway' 开始API测试{Style.RESET_ALL}")

    def emptyline(self):
        """处理空行"""
        pass

    def precmd(self, line: str) -> str:
        """预处理命令行输入，更新提示符"""
        if line.strip():
            self.command_count += 1

        status_info = ""
        if self.current_test_file:
            status_info = f"{Fore.GREEN}[{os.path.basename(self.current_test_file)}]{Style.RESET_ALL} "

        if self.session_vars:
            status_info += f"{Fore.BLUE}[{len(self.session_vars)}vars]{Style.RESET_ALL} "

        self.prompt = f"{status_info}{Fore.YELLOW + Style.BRIGHT}🚀 YH-API-Test{Fore.CYAN} >{Style.RESET_ALL} "

        line = line.strip()

        if line == "2":
            return "docs"
        elif line == "6":
            return "generate"

        return line


def main():
    """主函数"""
    try:
        shell = YHShell()
        shell.cmdloop()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW + Style.BRIGHT}🌟 YH精神永存！再见！{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ 程序异常: {e}{Style.RESET_ALL}")


def fadeaway_main():
    """fadeaway命令入口点"""
    try:
        shell = YHShell()
        shell.do_fadeaway("")
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW + Style.BRIGHT}🌟 YH精神永存！再见！{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ fadeaway执行异常: {e}{Style.RESET_ALL}")


def inspire_main():
    """inspire命令入口点"""
    try:
        shell = YHShell()
        shell.do_inspire("")
    except Exception as e:
        print(f"\n{Fore.RED}❌ inspire执行异常: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
