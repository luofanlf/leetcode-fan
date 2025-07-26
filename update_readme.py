#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys
from pathlib import Path

def extract_problem_info(filename):
    """从文件名中提取题号和题目名称"""
    # 匹配形如 "27.移除元素.md" 的文件名
    match = re.match(r'^(\d+)\.(.+)\.md$', filename)
    if match:
        problem_id = int(match.group(1))
        problem_name = match.group(2)
        return problem_id, problem_name
    return None, None

def get_category_emoji(category_name):
    """根据分类名称返回对应的emoji"""
    emoji_map = {
        '数组': '🔢',
        '链表': '🔗',
        '栈': '📚',
        '队列': '🚶',
        '树': '🌳',
        '图': '🗺️',
        '动态规划': '🧠',
        '贪心': '💡',
        '回溯': '🔄',
        '二分查找': '🔍',
        '排序': '📊',
        '字符串': '📝',
        '哈希表': '🗂️',
        '双指针': '👆',
        '滑动窗口': '🪟'
    }
    return emoji_map.get(category_name, '📁')

def scan_problems():
    """扫描src目录下的所有题解文件"""
    src_path = Path('src')
    if not src_path.exists():
        print("错误：找不到src目录")
        return {}
    
    categories = {}
    
    # 遍历所有子目录
    for category_dir in src_path.iterdir():
        if category_dir.is_dir() and not category_dir.name.startswith('.'):
            category_name = category_dir.name
            problems = []
            
            # 遍历分类目录下的所有文件
            for file_path in category_dir.iterdir():
                if file_path.is_file() and file_path.name.endswith('.md'):
                    problem_id, problem_name = extract_problem_info(file_path.name)
                    if problem_id is not None:
                        problems.append({
                            'id': problem_id,
                            'name': problem_name,
                            'filename': file_path.name,
                            'path': str(file_path).replace('\\', '/')
                        })
            
            # 按题号排序
            problems.sort(key=lambda x: x['id'])
            categories[category_name] = problems
    
    return categories

def generate_readme(categories):
    """生成README.md内容"""
    content = """# LeetCode 刷题笔记

这个项目用于记录我的LeetCode刷题思路和题解，按照算法和数据结构的类型进行分类整理。

## 项目结构

题解按照数据结构和算法类型进行分类，每个分类对应一个文件夹，包含相关题目的详细解答和思路分析。

---

## 📂 题目分类

"""
    
    # 按分类名称排序
    sorted_categories = sorted(categories.items())
    
    for category_name, problems in sorted_categories:
        if not problems:  # 跳过空分类
            continue
            
        emoji = get_category_emoji(category_name)
        content += f"### {emoji} {category_name}\n\n"
        content += "| 题号 | 题目 | 解答 |\n"
        content += "|------|------|------|\n"
        
        for problem in problems:
            content += f"| {problem['id']} | {problem['name']} | [{problem['path']}]({problem['path']}) |\n"
        
        content += "\n"
    
    content += """---

## 📝 说明

每个题解文件包含：
- 题目描述和要求
- 解题思路分析
- 代码实现（主要使用Java）
- 时间复杂度和空间复杂度分析
- 关键点和注意事项

## 🎯 学习目标

通过系统性的刷题和总结，掌握常见的算法和数据结构，提高编程能力和问题解决思维。

---

*持续更新中...*"""
    
    return content

def update_readme():
    """更新README.md文件"""
    print("🔍 扫描题解文件...")
    categories = scan_problems()
    
    if not categories:
        print("❌ 没有找到任何题解文件")
        return False
    
    # 统计题目数量
    total_problems = sum(len(problems) for problems in categories.values())
    print(f"📊 找到 {len(categories)} 个分类，共 {total_problems} 道题目")
    
    for category_name, problems in categories.items():
        print(f"  - {category_name}: {len(problems)} 道题")
    
    print("📝 生成README.md...")
    content = generate_readme(categories)
    
    # 写入README.md文件
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md 更新完成")
    return True

def commit_to_git():
    """提交更改到Git"""
    try:
        print("📤 准备提交到Git...")
        
        # 检查是否有未提交的更改
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("ℹ️  没有需要提交的更改")
            return True
        
        # 添加所有更改
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ 文件已添加到暂存区")
        
        # 生成提交信息
        commit_message = "📚 更新README: 自动扫描并同步题解目录"
        
        # 提交更改
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"✅ 提交完成: {commit_message}")
        
        # 推送到远程仓库
        print("🚀 推送到远程仓库...")
        subprocess.run(['git', 'push'], check=True)
        print("✅ 推送完成")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 未找到Git命令，请确保已安装Git")
        return False

def main():
    """主函数"""
    print("🚀 开始自动更新README...")
    
    # 检查是否在正确的目录
    if not os.path.exists('src'):
        print("❌ 错误：请在项目根目录下运行此脚本")
        sys.exit(1)
    
    # 更新README
    if not update_readme():
        sys.exit(1)
    
    # 提交到Git
    if not commit_to_git():
        print("⚠️  README已更新，但Git提交失败")
        sys.exit(1)
    
    print("🎉 任务完成！README已更新并提交到GitHub")

if __name__ == "__main__":
    main() 