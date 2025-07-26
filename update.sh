#!/bin/bash

# LeetCode题解自动更新脚本
# 用途：自动扫描题解文件并更新README，然后提交到GitHub

echo "🚀 启动LeetCode题解自动更新..."

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到python3，请先安装Python 3"
    exit 1
fi

# 运行Python更新脚本
python3 update_readme.py

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "🎉 自动更新完成！"
else
    echo "❌ 更新失败，请检查错误信息"
    exit 1
fi 