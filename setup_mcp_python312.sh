#!/bin/bash
# MCP服务器设置脚本 - 使用Python 3.12

echo "=== MCP服务器设置 - Python 3.12 ==="

# 设置路径
PYTHON_PATH="/Users/code/miniconda3/bin/python3.12"
SERVER_PATH="/Users/code/git/Skill_Seekers_fork/src/skill_seekers/mcp/server.py"
WRAPPER_PATH="/Users/code/git/Skill_Seekers_fork/python3_wrapper.sh"

# 确保Python 3.12安装了mcp包
echo "安装mcp包..."
$PYTHON_PATH -m pip install mcp

# 安装项目依赖
echo "安装项目依赖..."
$PYTHON_PATH -m pip install -r /Users/code/git/Skill_Seekers_fork/requirements.txt

# 更新包装脚本
echo "更新Python包装脚本..."
echo "#!/bin/bash
# Python 3包装脚本，确保使用Python 3.12

$PYTHON_PATH \"\$@\"" > $WRAPPER_PATH

chmod +x $WRAPPER_PATH

# 创建统一的配置文件
echo "创建MCP配置文件..."
CONFIG_DIRS=("~/.claude" "~/.config/claude-code")
CONFIG_CONTENT='{"mcpServers":{"skill-seeks":{"command":"'$WRAPPER_PATH'","args":["'$SERVER_PATH'"],"cwd":"/Users/code/git/Skill_Seekers_fork","env":{}}}}'

for dir in "${CONFIG_DIRS[@]}"; do
  mkdir -p $(eval echo $dir)
  echo $CONFIG_CONTENT > $(eval echo $dir)/mcp.json
  echo "已创建 $dir/mcp.json"
done

# 终止所有Claude进程
echo "终止Claude进程..."
pkill -f claude || echo "没有发现Claude进程"

# 等待几秒钟
sleep 3

echo "=== 设置完成 ==="
echo "请运行 'claude mcp list' 测试连接"
