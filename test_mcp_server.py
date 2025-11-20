#!/usr/bin/env python3
import socket
import time

# 尝试连接MCP服务器（默认端口通常是7500）
def test_mcp_connection():
    host = 'localhost'
    port = 7500
    
    print(f"正在测试连接到 {host}:{port}...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((host, port))
            if result == 0:
                print("✅ 成功连接到MCP服务器！")
                return True
            else:
                print(f"❌ 无法连接到服务器。错误码: {result}")
                return False
    except Exception as e:
        print(f"❌ 连接测试时出错: {e}")
        return False

if __name__ == "__main__":
    print("MCP服务器连接测试")
    print("-" * 30)
    success = test_mcp_connection()
    
    if not success:
        print("\n服务器可能没有运行或者使用不同的端口。")
        print("请确保服务器已使用Python 3.12启动，并且mcp包已正确安装。")