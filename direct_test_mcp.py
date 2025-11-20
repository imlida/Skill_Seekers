#!/usr/bin/env python3
import subprocess
import sys
import time
import json

# 使用Python 3.12直接测试MCP服务器
def test_mcp_directly():
    python_path = "/Users/code/miniconda3/bin/python3.12"
    server_script = "/Users/code/git/Skill_Seekers_fork/src/skill_seekers/mcp/server.py"
    
    print(f"正在使用 {python_path} 测试MCP服务器...")
    print("注意：MCP服务器设计为与Claude Code通过标准输入/输出通信")
    print("这个测试将验证服务器能否正确加载并响应基本命令")
    
    try:
        # 创建一个简单的测试命令（初始化）
        test_input = json.dumps({
            "type": "initialize",
            "params": {}
        }) + "\n"
        
        # 启动服务器进程
        print(f"\n启动服务器: {python_path} {server_script}")
        process = subprocess.Popen(
            [python_path, server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 发送初始化命令
        print("\n发送初始化命令...")
        process.stdin.write(test_input)
        process.stdin.flush()
        
        # 给服务器一点时间响应
        time.sleep(2)
        
        # 尝试读取输出（非阻塞）
        try:
            stdout_data = process.stdout.readline(1024)
            stderr_data = process.stderr.read(1024)
            
            print("\n服务器标准输出:")
            if stdout_data:
                print(stdout_data)
            else:
                print("无输出")
                
            print("\n服务器标准错误:")
            if stderr_data:
                print(stderr_data)
            else:
                print("无错误")
                
            # 检查是否有模块导入错误
            if "ImportError" in stderr_data or "ModuleNotFoundError" in stderr_data:
                print("\n❌ 发现导入错误，请确保mcp包已正确安装到Python 3.12环境")
                return False
                
            print("\n✅ 服务器似乎已成功启动，没有明显错误")
            return True
            
        finally:
            # 清理进程
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        return False

if __name__ == "__main__":
    print("MCP服务器直接测试")
    print("=" * 50)
    
    success = test_mcp_directly()
    
    if success:
        print("\n" + "=" * 50)
        print("下一步建议:")
        print("1. 完全退出Claude Code应用程序")
        print("2. 重新启动Claude Code")
        print("3. 再次运行 'claude mcp list' 测试连接")
        print("4. 如果仍有问题，请检查配置文件路径是否正确")
    else:
        print("\n" + "=" * 50)
        print("问题解决步骤:")
        print(f"1. 确认mcp包已安装: {python_path} -m pip install mcp")
        print("2. 检查Claude Code配置文件是否正确更新")
        print("3. 确认配置文件路径是否为: ~/.config/claude-code/mcp.json")