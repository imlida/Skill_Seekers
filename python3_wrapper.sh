#!/bin/bash
# Python 3包装脚本，确保使用Python 3.12
# 创建临时目录并添加 python3 符号链接指向 Python 3.12
mkdir -p /tmp/bin
ln -sf /Users/code/miniconda3/bin/python3.12 /tmp/bin/python3

# 修改 PATH 环境变量
export PATH="/tmp/bin:$PATH"

/Users/code/miniconda3/bin/python3.12 "$@"
