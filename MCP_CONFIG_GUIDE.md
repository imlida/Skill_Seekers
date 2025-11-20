# MCP服务器配置指南

## 问题分析

在尝试运行Skill Seekers的MCP服务器时，我们遇到了以下主要问题：

1. **Python版本不兼容**：系统默认Python版本为3.9.6，而`mcp`包要求Python 3.10或更高版本
2. **Claude Code配置问题**：Claude Code默认使用`python3`命令（指向系统Python 3.9.6）
3. **服务器通信方式**：MCP服务器使用标准输入/输出(stdio)进行通信，而不是TCP端口

## 解决方案

### 1. 已完成的设置

- ✅ 已确认系统中存在Python 3.12: `/Users/code/miniconda3/bin/python3.12`
- ✅ 已使用Python 3.12安装了`mcp`包及其依赖
- ✅ 已创建了自定义配置脚本`setup_mcp_python312.sh`
- ✅ 已在`~/.claude/mcp.json`中创建了正确的MCP配置文件
- ✅ 直接测试显示服务器能在Python 3.12环境中正常启动并响应JSON-RPC请求
- ✅ 已安装项目所有依赖: `pip install -r requirements.txt`

### 2. 确保Claude Code正确配置

根据测试结果，MCP服务器本身可以正常工作。现在需要确保Claude Code正确使用新的配置：

1. **完全退出Claude Code**（重要！）
   - 在Mac上：点击菜单栏的Claude Code图标，选择「退出」
   - 或者使用Command+Q完全关闭应用程序

2. **验证配置文件**：确认`~/.claude/mcp.json`包含以下内容：

```json
{
  "mcpServers": {
    "skill-seeks": {
      "command": "/Users/code/miniconda3/bin/python3.12",
      "args": [
        "/Users/code/git/Skill_Seekers_fork/src/skill_seekers/mcp/server.py"
      ],
      "cwd": "/Users/code/git/Skill_Seekers_fork",
      "env": {}
    }
  }
}
```

如果文件不存在，可以使用以下命令创建：
```bash
mkdir -p ~/.claude
cat > ~/.claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "skill-seeks": {
      "command": "/Users/code/miniconda3/bin/python3.12",
      "args": [
        "/Users/code/git/Skill_Seekers_fork/src/skill_seekers/mcp/server.py"
      ],
      "cwd": "/Users/code/git/Skill_Seekers_fork",
      "env": {}
    }
  }
}
EOF
```

3. **重新启动Claude Code**
   - 等待应用程序完全启动

### 3. 测试连接

重启Claude Code后，在终端中运行：

```bash
claude mcp list
```

如果配置正确，您应该看到服务器状态显示为已连接。

### 4. 高级故障排除

如果仍然遇到问题，请尝试以下步骤：

1. **修改环境变量** (推荐解决方案)：
   通过测试发现，最可靠的解决方案是临时修改 PATH 环境变量，确保 `python3` 命令指向 Python 3.12：
   
   ```bash
   # 创建临时目录并添加 python3 符号链接指向 Python 3.12
   mkdir -p /tmp/bin
   ln -sf /Users/code/miniconda3/bin/python3.12 /tmp/bin/python3
   
   # 修改 PATH 环境变量
   export PATH="/tmp/bin:$PATH"
   
   # 验证 Python 版本
   python3 --version  # 应该显示 Python 3.12.x
   
   # 现在测试连接
   claude mcp list
   ```
   
   对于永久性解决方案，可以：
   - 将以上命令添加到你的 `.bashrc` 或 `.zshrc` 文件中
   - 或者在每次使用 Claude MCP 功能前运行这个脚本

2. **验证配置文件**：
   ```bash
   cat ~/.claude/mcp.json
   ```

3. **验证Python环境**：
   ```bash
   /Users/code/miniconda3/bin/python3.12 -c "import mcp; print('mcp包已正确安装，Python版本:', __import__('sys').version)"
   ```

4. **使用全面测试脚本**：
   ```bash
   python3 /Users/code/git/Skill_Seekers_fork/comprehensive_mcp_test.py
   ```
   这个脚本会自动检查mcp包、安装项目依赖、测试服务器响应。

5. **检查Claude Code是否完全退出**：
   ```bash
   # 检查是否有Claude相关进程在运行
   ps aux | grep -i claude
   ```
   如果有进程在运行，可以使用Activity Monitor终止它们。

6. **重新创建配置文件**：完全删除配置文件后重新创建
   ```bash
   rm ~/.claude/mcp.json
   # 然后重新创建配置文件（使用上面的命令）
   ```

7. **检查项目依赖**：
   ```bash
   /Users/code/miniconda3/bin/python3.12 -m pip install -r /Users/code/git/Skill_Seekers_fork/requirements.txt
   ```

8. **检查Claude Code版本**：确保您使用的是最新版本的Claude Code。

9. **查看Claude Code日志**：在应用程序中查找详细的错误日志信息。

## 注意事项

- MCP服务器设计为通过标准输入/输出与Claude Code通信，而不是作为独立的网络服务器
- 不要尝试直接运行server.py并期望它监听TCP端口
- Claude Code会自动管理服务器进程的启动和停止

完成上述配置后，Skill Seekers的MCP功能应该能够正常工作。