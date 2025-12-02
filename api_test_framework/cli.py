#!/usr/bin/env python3
"""
API测试框架CLI入口
提供命令行接口
"""

import sys
import os
from pathlib import Path

# 将源码目录添加到Python路径
source_dir = Path(__file__).parent.parent
if str(source_dir) not in sys.path:
    sys.path.insert(0, str(source_dir))

def main():
    """主入口函数"""
    try:
        # 导入YHShell
        from yh_shell import main as yh_main
        yh_main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已正确安装api-test-yh-pro包")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
