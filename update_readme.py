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
        '二叉树': '🌳',
        '图': '🗺️',
        '动态规划': '🧠',
        '贪心': '💡',
        '回溯': '🔄',
        '二分查找': '🔍',
        '排序': '📊',
        '字符串': '📝',
        '哈希': '🗂️',
        '双指针': '👆',
        '滑动窗口': '🪟',
        '子串': '👦',
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
                    # 过滤掉以"0."开头的文件（题型总结）
                    if problem_id is not None and problem_id != 0:
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
    # 计算统计信息
    total_problems = sum(len(problems) for problems in categories.values())
    total_categories = len(categories)
    
    content = """# LeetCode 刷题笔记

这个项目用于记录我的LeetCode刷题思路和题解，按照算法和数据结构的类型进行分类整理。

## 📊 刷题统计

| 统计项 | 数量 |
|--------|------|
| 总题目数 | {} |
| 已完成分类 | {} |
| 平均每类题目数 | {:.1f} |

## 题目分类概览

""".format(total_problems, total_categories, total_problems / total_categories if total_categories > 0 else 0)

    # 添加分类概览
    content += "| 分类 | 题目数 | 完成度 |\n"
    content += "|------|--------|--------|\n"
    
    for category_name, problems in sorted(categories.items()):
        problem_count = len(problems)
        completion_rate = "100%" if problem_count > 0 else "0%"
        emoji = get_category_emoji(category_name)
        content += f"| {emoji} {category_name} | {problem_count} | {completion_rate} |\n"
    
    content += """

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

*持续更新中...*"""
    
    return content

def parse_existing_readme():
    """解析现有README文件中的题目"""
    existing_problems = set()
    
    if not os.path.exists('README.md'):
        return existing_problems
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式匹配表格中的题目行
        # 匹配形如 "| 27 | 移除元素 | [src/数组/27.移除元素.md](src/数组/27.移除元素.md) |"
        pattern = r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|'
        matches = re.findall(pattern, content)
        
        for match in matches:
            problem_id = int(match[0])
            problem_name = match[1].strip()
            existing_problems.add((problem_id, problem_name))
    
    except Exception as e:
        print(f"⚠️  解析现有README时出错: {e}")
    
    return existing_problems

def find_new_problems(current_categories, existing_problems):
    """找出新添加的题目"""
    new_problems = []
    
    for category_name, problems in current_categories.items():
        for problem in problems:
            problem_tuple = (problem['id'], problem['name'])
            if problem_tuple not in existing_problems:
                new_problems.append(problem)
    
    return new_problems

def update_readme():
    """更新README.md文件"""
    print("🔍 扫描题解文件...")
    
    # 解析现有README中的题目
    existing_problems = parse_existing_readme()
    
    # 扫描当前题目
    categories = scan_problems()
    
    if not categories:
        print("❌ 没有找到任何题解文件")
        return False, []
    
    # 找出新增题目
    new_problems = find_new_problems(categories, existing_problems)
    
    # 统计题目数量
    total_problems = sum(len(problems) for problems in categories.values())
    print(f"📊 找到 {len(categories)} 个分类，共 {total_problems} 道题目")
    
    if new_problems:
        print(f"🆕 发现 {len(new_problems)} 道新题目:")
        for problem in new_problems:
            print(f"  - {problem['id']}.{problem['name']}")
    
    for category_name, problems in categories.items():
        print(f"  - {category_name}: {len(problems)} 道题")
    
    print("📝 生成README.md...")
    content = generate_readme(categories)
    
    # 写入README.md文件
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md 更新完成")
    return True, new_problems

def commit_to_git(new_problems):
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
        if new_problems:
            # 如果有新题目，列出新题目的名字
            problem_names = [f"{problem['id']}.{problem['name']}" for problem in new_problems]
            if len(problem_names) == 1:
                commit_message = f"add {problem_names[0]}"
            else:
                commit_message = f"add {', '.join(problem_names)}"
        else:
            # 如果没有新题目，使用通用信息
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
    success, new_problems = update_readme()
    if not success:
        sys.exit(1)
    
    # 只有当有新题目时才执行Git操作
    if new_problems:
        print(f"🔄 检测到 {len(new_problems)} 道新题目，准备提交到Git...")
        if not commit_to_git(new_problems):
            print("⚠️  README已更新，但Git提交失败")
            sys.exit(1)
        print("🎉 任务完成！README已更新并提交到GitHub")
    else:
        print("ℹ️  没有新题目，跳过Git操作")
        print("✅ README检查完成，所有题目已是最新状态")

if __name__ == "__main__":
    main() 