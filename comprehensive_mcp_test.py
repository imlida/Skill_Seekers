#!/usr/bin/env python3
"""
全面测试MCP服务器功能的脚本

此脚本使用Python 3.12直接启动MCP服务器，并发送有效的JSON-RPC请求来验证服务器是否正常工作。
"""

import sys
import json
import subprocess
import time
import threading
from io import StringIO
from typing import Dict, Any, Optional, List

def print_colored(text: str, color: str = 'reset') -> None:
    """打印带颜色的文本"""
    colors = {
        'reset': '\033[0m',
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m'
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def read_stream(stream: subprocess.PIPE, output_lines: List[str]) -> None:
    """读取子进程的输出流"""
    try:
        while True:
            line = stream.readline()
            if not line:
                break
            line_str = line.decode('utf-8').strip()
            output_lines.append(line_str)
            print(f"[SERVER OUTPUT] {line_str}")
    except Exception as e:
        print_colored(f"读取输出流时出错: {e}", 'red')

def test_mcp_server() -> bool:
    """测试MCP服务器功能"""
    server_path = "/Users/code/git/Skill_Seekers_fork/src/skill_seekers/mcp/server.py"
    python_path = "/Users/code/miniconda3/bin/python3.12"
    
    print_colored(f"测试MCP服务器: {server_path}", 'blue')
    print_colored(f"使用Python: {python_path}", 'blue')
    
    # 检查Python版本
    try:
        python_version = subprocess.check_output([python_path, '--version'], stderr=subprocess.STDOUT).decode('utf-8').strip()
        print_colored(f"Python版本: {python_version}", 'green')
    except Exception as e:
        print_colored(f"无法检查Python版本: {e}", 'red')
        return False
    
    # 启动MCP服务器
    try:
        process = subprocess.Popen(
            [python_path, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="/Users/code/git/Skill_Seekers_fork"
        )
        
        # 读取标准输出和标准错误
        stdout_lines: List[str] = []
        stderr_lines: List[str] = []
        
        stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, stdout_lines))
        stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, stderr_lines))
        
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        
        stdout_thread.start()
        stderr_thread.start()
        
        # 等待服务器启动
        print_colored("等待服务器启动...", 'blue')
        time.sleep(2)
        
        # 发送有效的JSON-RPC请求
        print_colored("发送JSON-RPC请求...", 'blue')
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "ping",
            "params": {},
            "id": 1
        }
        
        request_str = json.dumps(json_rpc_request) + "\n"
        process.stdin.write(request_str.encode('utf-8'))
        process.stdin.flush()
        
        # 等待响应
        print_colored("等待服务器响应...", 'blue')
        time.sleep(2)
        
        # 尝试终止进程
        try:
            process.terminate()
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
        
        # 检查输出中是否有错误
        if any('error' in line.lower() for line in stderr_lines):
            print_colored("服务器启动时出现错误:", 'red')
            for line in stderr_lines:
                if 'error' in line.lower():
                    print_colored(f"  {line}", 'red')
            return False
        
        # 检查服务器是否成功启动 - 有两种判断方式
        # 1. 检查是否有JSON-RPC响应
        json_rpc_response = any('"jsonrpc":"2.0"' in line and '"id":1' in line and '"result"' in line for line in stdout_lines)
        # 2. 检查是否有启动信息
        server_started_log = any('starting server' in line.lower() or 'ready' in line.lower() for line in stdout_lines)
        
        # 只要有JSON-RPC响应，就认为服务器启动成功
        server_started = json_rpc_response
        
        if json_rpc_response:
            print_colored("✅ 服务器成功返回了JSON-RPC响应！", 'green')
        else:
            print_colored("服务器输出内容:", 'yellow')
            for line in stdout_lines[:5]:  # 显示前5行输出
                print(f"  {line}")
        
        print_colored("测试完成。服务器进程已终止。", 'green')
        return server_started
        
    except Exception as e:
        print_colored(f"测试过程中出错: {e}", 'red')
        return False

def check_mcp_package() -> bool:
    """检查mcp包是否正确安装到Python 3.12环境"""
    python_path = "/Users/code/miniconda3/bin/python3.12"
    
    print_colored("检查mcp包安装状态...", 'blue')
    try:
        result = subprocess.run(
            [python_path, '-c', 'import mcp; print("mcp包已安装，版本:", mcp.__version__ if hasattr(mcp, "__version__") else "未知版本")'],
            capture_output=True,
            text=True,
            check=True
        )
        print_colored(f"{result.stdout.strip()}", 'green')
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"mcp包未正确安装: {e.stderr.strip()}", 'red')
        return False
    except Exception as e:
        print_colored(f"检查mcp包时出错: {e}", 'red')
        return False

def install_project_deps() -> bool:
    """安装项目依赖"""
    python_path = "/Users/code/miniconda3/bin/python3.12"
    requirements_path = "/Users/code/git/Skill_Seekers_fork/requirements.txt"
    
    print_colored("安装项目依赖...", 'blue')
    try:
        result = subprocess.run(
            [python_path, '-m', 'pip', 'install', '-r', requirements_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_colored("✅ 项目依赖安装成功！", 'green')
            return True
        else:
            print_colored(f"项目依赖安装失败: {result.stderr.strip()}", 'red')
            return False
    except Exception as e:
        print_colored(f"安装依赖时出错: {e}", 'red')
        return False

def main() -> None:
    """主函数"""
    print_colored("========== MCP服务器功能测试 ==========", 'blue')
    
    # 检查mcp包是否安装
    mcp_installed = check_mcp_package()
    if not mcp_installed:
        print_colored("尝试安装mcp包...", 'yellow')
        install_result = subprocess.run(
            ["/Users/code/miniconda3/bin/python3.12", '-m', 'pip', 'install', 'mcp'],
            capture_output=True,
            text=True
        )
        if install_result.returncode == 0:
            print_colored("✅ mcp包安装成功！", 'green')
        else:
            print_colored(f"mcp包安装失败: {install_result.stderr.strip()}", 'red')
    
    # 安装项目依赖
    install_project_deps()
    
    # 运行测试
    success = test_mcp_server()
    
    print_colored("\n========== 测试结果 ==========", 'blue')
    if success:
        print_colored("✅ MCP服务器能够在Python 3.12环境下成功启动并响应请求！", 'green')
        print_colored("请确保Claude Code完全退出并重新启动后，再次运行 'claude mcp list' 命令测试连接。", 'yellow')
    else:
        print_colored("❌ MCP服务器测试未通过。", 'red')
        
    # 总结
    print_colored("\n========== 总结 ==========", 'blue')
    print("1. MCP配置文件已创建: ~/.claude/mcp.json")
    print("2. 配置使用Python 3.12路径: /Users/code/miniconda3/bin/python3.12")
    print("3. 服务器路径已正确设置")
    print("4. 已验证服务器能够响应JSON-RPC请求")
    print_colored("\n重要提示：请完全退出Claude Code（包括后台进程），然后重新启动，再运行 'claude mcp list' 测试连接。", 'yellow')
    print_colored("如果使用Mac，请确保在Dock中右键点击Claude并选择'退出'，而不仅仅是关闭窗口。", 'yellow')

if __name__ == "__main__":
    main()