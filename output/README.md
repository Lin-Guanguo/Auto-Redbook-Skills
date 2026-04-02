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

## 产出记录

| # | 目录 | 文章 | 渲染系统 | 主题 | 页数 | 日期 | 状态 |
|---|------|------|----------|------|------|------|------|
| 1 | `blog-ai-crisis` | AI 经济危机推演 | legacy (`render_xhs.py`) | `wenkai` | 12 | 2026-03-22 | 已发布 |
| 2 | `blog-ai-pyramid` | AI 金字塔 | legacy | `wenkai` | — | 2026-03-22 | 已渲染 |
| 3 | `anthropic-blog-analysis` | Anthropic 博客分析 | legacy | — | — | 2026-03 | 已渲染 |
| 4 | `blog-python-type-system` | Python 类型系统（旧版） | legacy | — | — | 2026-03 | 已归档 |
| 5 | `ai-tech-debt` | AI 写代码很强，又微妙地不行 | new (`render.py`) | `block` | 18 | 2026-03-28 | 已发布 |
| 6 | `python-type-blog` | 第一次写 Python 项目，一些发现 | new | `paper` | 15 | 2026-03-27 | 已发布 |
| 7 | `python-type-blog-slab` | （同上，slab 主题测试） | new | `slab` | 19 | 2026-03-30 | 测试 |
| 8 | `agent-context-memory` | 6 个 Agent 上下文与记忆系统对比 | new | `slab` | 18 | 2026-03-30 | 待发布 |

### 主题使用记录

| 主题 | 风格 | 渲染系统 | 用过的文章 |
|------|------|----------|-----------|
| `wenkai` | 文楷书卷风：霞鹜文楷 + 宣纸底 + 朱砂红 | legacy | #1, #2 |
| `paper` | 笔记纸：横线纸 + 左侧红线 + 暖纸底 | new | #6 |
| `block` | 色块风：藏蓝+靛蓝冷色大色块，现代编辑感 | new | #5 |
| `slab` | 厚板风：森绿+赤陶暖色大色块，杂志编辑感 | new | #7, #8 |

## 下次改进考虑

- **卡片外框差异化**：当前所有卡片的外层容器结构一致（底边渐变 + 固定大小圆角内卡），辨识度高。下次考虑改变内卡的大小、圆角、边距或去掉内卡，让不同主题的卡片结构本身也有区别，而不只是配色不同。

## 个人偏好

- **首选主题**：`block`（冷色大色块）/ `slab`（暖色大色块）/ `paper`（笔记纸）
- **首选渲染系统**：new (`render.py`)，自动分页
- **内容语言**：中文
- **内容风格**：技术分析类，结构清晰，善用表格和代码块呈现信息
- **标题风格**：简洁直接，不用夸张标题党
- **渲染命令**：
  ```bash
  # 标准 (3:4)
  python scripts/render.py output/{topic}/input.md --style slab -o output/{topic}
  # 长页 (接近 9:16，适合表格多的长文)
  python scripts/render.py output/{topic}/input.md --style slab --height 2020 -o output/{topic}
  ```
