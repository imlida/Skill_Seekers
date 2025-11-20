#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试MCP服务器的脚本，通过标准输入/输出通信
"""

import subprocess
import json
import time
import sys

# 设置路径
PYTHON_PATH = "/Users/code/miniconda3/bin/python3.12"
SERVER_PATH = "/Users/code/git/Skill_Seekers_fork/src/skill_seekers/mcp/server.py"
CWD = "/Users/code/git/Skill_Seekers_fork"

def run_direct_test():
    """直接测试MCP服务器的标准输入/输出通信"""
    print("\033[1;34m========== MCP服务器直接通信测试 ==========\033[0m")
    
    try:
        # 启动服务器进程
        print(f"启动服务器: {PYTHON_PATH} {SERVER_PATH}")
        process = subprocess.Popen(
            [PYTHON_PATH, SERVER_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=CWD,
            text=True
        )
        
        # 等待服务器启动
        time.sleep(2)
        
        # 构建JSON-RPC请求
        request = {
            "jsonrpc": "2.0",
            "method": "ping",
            "id": 1
        }
        
        # 发送请求
        request_str = json.dumps(request) + "\n"
        print(f"发送请求: {request_str.strip()}")
        process.stdin.write(request_str)
        process.stdin.flush()
        
        # 读取响应
        print("等待响应...")
        
        # 设置超时
        start_time = time.time()
        timeout = 5
        response_lines = []
        
        while True:
            # 检查进程是否已终止
            if process.poll() is not None:
                print("\033[1;31m❌ 服务器进程意外终止\033[0m")
                stderr = process.stderr.read()
                if stderr:
                    print(f"\033[1;31m服务器错误输出:\n{stderr}\033[0m")
                break
            
            # 检查超时
            if time.time() - start_time > timeout:
                print("\033[1;31m❌ 响应超时\033[0m")
                break
            
            # 尝试读取输出
            try:
                # 使用非阻塞读取的替代方法
                response_line = process.stdout.readline()
                if response_line:
                    response_lines.append(response_line.strip())
                    print(f"\033[1;32m接收到响应: {response_line.strip()}\033[0m")
                    
                    # 尝试解析JSON
                    try:
                        response_json = json.loads(response_line)
                        if "id" in response_json and response_json["id"] == 1:
                            print("\033[1;32m✅ 成功接收到有效的JSON-RPC响应\033[0m")
                            break
                    except json.JSONDecodeError:
                        print("\033[1;33m⚠️  接收到的不是有效的JSON\033[0m")
            except Exception as e:
                print(f"\033[1;31m读取输出时出错: {e}\033[0m")
                break
            
            time.sleep(0.1)
        
        # 终止进程
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
        
        # 检查是否有错误输出
        stderr = process.stderr.read()
        if stderr:
            print(f"\033[1;31m服务器错误输出:\n{stderr}\033[0m")
        
        return True if response_lines else False
        
    except Exception as e:
        print(f"\033[1;31m测试过程中发生错误: {e}\033[0m")
        return False

def main():
    """主函数"""
    success = run_direct_test()
    
    print("\n\033[1;34m========== 测试总结 ==========\033[0m")
    if success:
        print("\033[1;32m✅ 直接通信测试成功！服务器能够正确响应JSON-RPC请求。\033[0m")
        print("\n如果Claude Code仍然无法连接，请尝试以下步骤:")
        print("1. 完全退出Claude Code（包括后台进程）")
        print("2. 确保配置文件同时存在于 ~/.claude/mcp.json 和 ~/.config/claude-code/mcp.json")
        print("3. 重启Claude Code后再次尝试")
    else:
        print("\033[1;31m❌ 直接通信测试失败。请检查以下可能的问题:\033[0m")
        print("1. mcp包是否正确安装到Python 3.12环境")
        print("2. 项目依赖是否正确安装")
        print("3. 服务器代码是否有错误")

if __name__ == "__main__":
    main()