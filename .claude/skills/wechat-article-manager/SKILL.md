---
name: wechat-article-manager
description: 管理公众号文章记录，添加新文章到 JSON 和 Markdown 文档。使用场景：当用户提供公众号文章的标题、链接、发布日期和简介时，自动更新 `/Users/qiuhe/Documents/blog/公众号文章.json` 和 `/Users/qiuhe/Documents/blog/公众号文章.md` 两个文件。
---

# 公众号文章管理器

## 概述

这个 skill 用于添加新的公众号文章到记录文档中。用户提供文章的标题、链接、发布日期和简介后，skill 会同时更新 JSON 和 Markdown 两个文件。

## 使用流程

当用户要求添加公众号文章时：

1. 从用户处获取以下信息：
   - 文章标题
   - 文章链接
   - 发布日期（格式：YYYY.MM.DD，如 2026.03.11）
   - 文章简介

2. 读取现有的两个文件确认格式：
   - `/Users/qiuhe/Documents/blog/公众号文章.json`
   - `/Users/qiuhe/Documents/blog/公众号文章.md`

3. 使用以下两种方式之一添加文章：
   - 方式 A：直接编辑两个文件（推荐）
   - 方式 B：使用 scripts/add_article.py 脚本

## 直接编辑文件的方法

### 更新 JSON 文件

在 `articles` 数组末尾添加新文章对象：

```json
{
  "title": "文章标题",
  "link": "文章链接",
  "date": "2026.03.11",
  "introduction": "文章简介"
}
```

### 更新 Markdown 文件

在文件末尾添加新条目，格式如下：

```
# 标题：文章标题
- 链接：文章链接
- 日期：2026.03.11
- 介绍：文章简介
```

## 使用脚本的方法

如果需要使用脚本，可以运行：

```bash
python3 /Users/qiuhe/.claude/skills/wechat-article-manager/scripts/add_article.py "标题" "链接" "日期" "简介"
```

注意：使用脚本前确保参数中的引号正确转义。
