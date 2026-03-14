# Output - 小红书笔记产出管理

所有产出文章通过此目录统一管理。

## 目录结构

```
output/
├── README.md
└── {topic-name}/          # 按主题分类，每次一个主题
    ├── *.md               # 原材料 & 渲染用 Markdown
    └── {theme}[-variant]/ # 渲染产出图片（cover.png + card_*.png）
```

每个主题目录包含：
- **原材料**：输入的 Markdown 源文件
- **产出结果**：渲染生成的图片目录（按主题/变体命名）

## 个人偏好

- **首选主题**：`blueprint`（工程蓝图风格）
- **首选分页模式**：`auto-split`（自动分页，适合长文）
- **内容语言**：中文
- **内容风格**：技术分析类，结构清晰，善用表格和代码块呈现信息
- **标题风格**：简洁直接，不用夸张标题党
- **渲染命令常用组合**：
  ```bash
  python scripts/render_xhs.py output/{topic}/{file}.md -t blueprint -m auto-split -o output/{topic}/{output-dir}
  ```
