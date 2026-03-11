#!/usr/bin/env python3
"""
添加公众号文章到 JSON 和 Markdown 文件
"""

import json
import os
import sys

# 文件路径
JSON_FILE = '/Users/qiuhe/Documents/blog/公众号文章.json'
MD_FILE = '/Users/qiuhe/Documents/blog/公众号文章.md'


def add_to_json(title, link, date, introduction):
    """添加文章到 JSON 文件"""
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_article = {
        "title": title,
        "link": link,
        "date": date,
        "introduction": introduction
    }

    data['articles'].append(new_article)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_to_markdown(title, link, date, introduction):
    """添加文章到 Markdown 文件"""
    new_entry = f"\n# 标题：{title}\n- 链接：{link}\n- 日期：{date}\n- 介绍：{introduction}\n"

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.rstrip() + new_entry

    with open(MD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    if len(sys.argv) != 5:
        print("用法: python add_article.py <标题> <链接> <日期> <简介>")
        sys.exit(1)

    title = sys.argv[1]
    link = sys.argv[2]
    date = sys.argv[3]
    introduction = sys.argv[4]

    add_to_json(title, link, date, introduction)
    add_to_markdown(title, link, date, introduction)
    print("文章已成功添加！")


if __name__ == '__main__':
    main()
