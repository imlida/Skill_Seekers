#!/bin/bash

# MCP环境设置脚本
# 此脚本创建临时python3符号链接指向Python 3.12并设置环境变量
# 适用于解决Claude MCP连接问题

echo "=== MCP环境设置脚本 ==="
echo "目标：确保python3命令指向Python 3.12，解决Claude MCP连接问题"

# 创建临时目录和符号链接
echo "\n创建python3符号链接指向Python 3.12..."
mkdir -p /tmp/bin
ln -sf /Users/code/miniconda3/bin/python3.12 /tmp/bin/python3

# 设置PATH环境变量
echo "设置环境变量..."
export PATH="/tmp/bin:$PATH"

# 验证Python版本
echo "\n验证Python版本："
python3 --version

# 测试MCP连接
echo "\n测试MCP连接..."
claude mcp list

# 提供持久化选项
echo "\n=== 持久化解决方案 ==="
echo "要永久解决此问题，可以将以下命令添加到您的shell配置文件中："
echo ""
echo "# 添加到 ~/.bashrc 或 ~/.zshrc 的内容："
echo "mkdir -p /tmp/bin"
echo "ln -sf /Users/code/miniconda3/bin/python3.12 /tmp/bin/python3"
echo "export PATH=\"/tmp/bin:$PATH\""
echo ""
echo "或者，您可以直接运行此脚本来临时修复问题。"
echo ""
echo "=== 设置完成 ==="