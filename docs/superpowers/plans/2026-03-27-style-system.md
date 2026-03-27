# Style System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** New rendering system with self-contained Python styles, starting with a Paper (笔记纸) style, completely separate from the old theme system.

**Architecture:** Each style is a Python module exporting `generate_cover()` and `generate_card()` that return complete HTML. A new `render.py` entry point handles CLI, markdown parsing, content splitting, and Playwright rendering. Old code untouched.

**Tech Stack:** Python 3, Playwright (chromium), markdown library, PyYAML

**Spec:** `docs/2026-03-27-style-system-design.md`

---

### Task 1: Create `scripts/styles/base.py` — Shared Utilities

**Files:**
- Create: `scripts/styles/base.py`

- [ ] **Step 1: Create the file with all utility functions**

```python
"""Shared utilities for style modules."""

import re
from typing import List

import markdown
import yaml


def css_reset() -> str:
    return "* { margin: 0; padding: 0; box-sizing: border-box; }"


def font_imports(fonts: List[str]) -> str:
    urls = []
    for font in fonts:
        name = font.replace(" ", "+")
        urls.append(
            f"@import url('https://fonts.googleapis.com/css2?"
            f"family={name}:wght@300;400;500;700;900&display=swap');"
        )
    return "\n".join(urls)


def html_document(body: str, styles: str, width: int, scripts: str = "") -> str:
    script_tag = f"<script>{scripts}</script>" if scripts else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width={width}">
    <style>
{styles}
    </style>
</head>
<body>
{body}
{script_tag}
</body>
</html>"""


def convert_markdown_to_html(md_content: str) -> str:
    # Extract tags (lines like #tag at end)
    tags_pattern = r'((?:#[\w\u4e00-\u9fa5]+\s*)+)$'
    tags_match = re.search(tags_pattern, md_content, re.MULTILINE)
    tags_html = ""

    if tags_match:
        tags_str = tags_match.group(1)
        md_content = md_content[:tags_match.start()].strip()
        tags = re.findall(r'#([\w\u4e00-\u9fa5]+)', tags_str)
        if tags:
            tags_html = '<div class="tags-container">'
            for tag in tags:
                tags_html += f'<span class="tag">#{tag}</span>'
            tags_html += "</div>"

    html = markdown.markdown(
        md_content,
        extensions=["extra", "codehilite", "tables", "nl2br"],
    )
    return html + tags_html


def title_font_size(title: str, width: int) -> int:
    length = len(title)
    if length <= 6:
        return int(width * 0.14)
    elif length <= 10:
        return int(width * 0.12)
    elif length <= 18:
        return int(width * 0.09)
    elif length <= 30:
        return int(width * 0.07)
    else:
        return int(width * 0.055)


def page_number_html(current: int, total: int) -> str:
    if total <= 1:
        return ""
    return f'<div class="page-number">{current}/{total}</div>'


def parse_markdown_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    yaml_pattern = r"^---\s*\n(.*?)\n---\s*\n"
    yaml_match = re.match(yaml_pattern, content, re.DOTALL)

    metadata = {}
    body = content

    if yaml_match:
        try:
            metadata = yaml.safe_load(yaml_match.group(1)) or {}
        except yaml.YAMLError:
            metadata = {}
        body = content[yaml_match.end() :]

    return {"metadata": metadata, "body": body.strip()}


def split_content_by_separator(body: str) -> List[str]:
    parts = re.split(r"\n---+\n", body)
    return [part.strip() for part in parts if part.strip()]
```

- [ ] **Step 2: Verify it imports cleanly**

Run: `cd /Users/linguanguo/dev/Auto-Redbook-Skills && python -c "import sys; sys.path.insert(0, 'scripts'); from styles.base import convert_markdown_to_html, parse_markdown_file; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/styles/base.py
git commit -m "feat: add styles/base.py with shared rendering utilities"
```

---

### Task 2: Create `scripts/styles/__init__.py` — Style Registry

**Files:**
- Create: `scripts/styles/__init__.py`

- [ ] **Step 1: Create the registry**

```python
"""Style registry. Each style is a Python module with generate_cover() and generate_card()."""


def get_style(name: str):
    """Returns the style module by name."""
    # Lazy imports to avoid circular dependencies
    if name == "paper":
        from styles import paper
        return paper
    raise ValueError(f"Unknown style: '{name}'. Available: paper")


def list_styles() -> list[str]:
    return ["paper"]
```

- [ ] **Step 2: Commit**

```bash
git add scripts/styles/__init__.py
git commit -m "feat: add style registry"
```

---

### Task 3: Create `scripts/styles/paper.py` — Paper Style

**Files:**
- Create: `scripts/styles/paper.py`

- [ ] **Step 1: Create the paper style module**

```python
"""Paper style — 笔记纸风格: horizontal ruled lines + left red margin line."""

from styles.base import (
    css_reset,
    font_imports,
    html_document,
    page_number_html,
    title_font_size,
)

STYLE_NAME = "paper"
STYLE_DESCRIPTION = "笔记纸风格 — 横线纸 + 左侧红线"


def _paper_css(width: int, height: int) -> str:
    line_height = int(height * 0.04)
    margin_left = int(width * 0.10)
    pad_left = int(width * 0.14)
    pad_right = int(width * 0.06)
    pad_top = int(height * 0.05)

    return f"""
{css_reset()}
{font_imports(["Noto Sans SC"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    width: {width}px;
    overflow: hidden;
    background: transparent;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: #f4f0e8;
    position: relative;
    padding: {pad_top}px {pad_right}px {pad_top}px {pad_left}px;
    background-image: linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px);
    background-size: 100% {line_height}px;
}}

.page::before {{
    content: '';
    position: absolute;
    top: 0;
    left: {margin_left}px;
    width: 2px;
    height: 100%;
    background: rgba(200, 100, 100, 0.35);
}}

/* Cover title */
.cover-title {{
    font-weight: 800;
    color: #2c2c2c;
    line-height: 1.3;
    margin-bottom: 20px;
}}

.cover-subtitle {{
    font-size: 38px;
    color: #999;
    font-style: italic;
    margin-bottom: 40px;
    line-height: 1.5;
}}

.cover-divider {{
    width: 60px;
    height: 3px;
    background: #c0392b;
    margin-bottom: 40px;
}}

/* Content typography */
.content {{
    color: #444;
    font-size: 42px;
    line-height: 1.8;
}}

.content h1 {{
    font-size: 72px;
    font-weight: 800;
    color: #2c2c2c;
    margin-bottom: 40px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 56px;
    font-weight: 700;
    color: #2c2c2c;
    margin: 50px 0 25px 0;
    line-height: 1.4;
}}

.content h3 {{
    font-size: 48px;
    font-weight: 600;
    color: #333;
    margin: 40px 0 20px 0;
}}

.content p {{
    margin-bottom: 35px;
}}

.content strong {{
    font-weight: 700;
    color: #2c2c2c;
}}

.content em {{
    font-style: italic;
    color: #c0392b;
}}

.content a {{
    color: #c0392b;
    text-decoration: none;
    border-bottom: 2px solid #c0392b;
}}

.content ul, .content ol {{
    margin: 30px 0;
    padding-left: 50px;
}}

.content li {{
    margin-bottom: 18px;
    line-height: 1.7;
}}

.content li::marker {{
    color: #c0392b;
}}

.content blockquote {{
    border-left: 6px solid #c0392b;
    padding: 25px 30px;
    color: #666;
    font-style: italic;
    margin: 35px 0;
    background: rgba(0, 0, 0, 0.02);
}}

.content blockquote p {{
    margin: 0;
}}

.content code {{
    background: rgba(0, 0, 0, 0.07);
    padding: 6px 14px;
    border-radius: 6px;
    font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    font-size: 36px;
    color: #555;
}}

.content pre {{
    background: #2c2c2c;
    color: #e0e0e0;
    padding: 40px;
    border-radius: 12px;
    margin: 35px 0;
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    font-size: 34px;
    line-height: 1.5;
}}

.content pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: inherit;
}}

.content hr {{
    border: none;
    height: 1px;
    background: rgba(0, 0, 0, 0.1);
    margin: 50px 0;
}}

.content img {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 35px auto;
    display: block;
}}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.04)}px;
    right: {pad_right}px;
    font-size: 32px;
    color: #aaa;
}}

.tags-container {{
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
}}

.tag {{
    display: inline-block;
    background: rgba(192, 57, 43, 0.1);
    color: #c0392b;
    padding: 10px 24px;
    border-radius: 20px;
    font-size: 32px;
    margin: 8px 12px 8px 0;
}}
"""


def generate_cover(
    title: str,
    subtitle: str,
    first_section_html: str,
    width: int,
    height: int,
) -> str:
    t_size = title_font_size(title, width)
    css = _paper_css(width, height)
    pad_top = int(height * 0.06)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>'

    body = f"""
    <div class="page">
        <div class="cover-title" style="font-size: {t_size}px; padding-top: {pad_top}px;">
            {title}
        </div>
        {subtitle_html}
        <div class="cover-divider"></div>
        <div class="content">{first_section_html}</div>
    </div>
    """
    return html_document(body, css, width)


def generate_card(
    content_html: str,
    page_number: int,
    total_pages: int,
    width: int,
    height: int,
) -> str:
    css = _paper_css(width, height)
    page_num = page_number_html(page_number, total_pages)

    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>
    """
    return html_document(body, css, width)
```

- [ ] **Step 2: Verify import**

Run: `cd /Users/linguanguo/dev/Auto-Redbook-Skills && python -c "import sys; sys.path.insert(0, 'scripts'); from styles.paper import generate_cover, generate_card; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/styles/paper.py
git commit -m "feat: add paper style (笔记纸)"
```

---

### Task 4: Create `scripts/render.py` — New Entry Point

**Files:**
- Create: `scripts/render.py`

- [ ] **Step 1: Create the rendering script**

```python
#!/usr/bin/env python3
"""
New rendering entry point for the style system.

Usage:
    python scripts/render.py input.md --style paper -o ./output
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Ensure styles package is importable
sys.path.insert(0, str(Path(__file__).parent))

from styles import get_style, list_styles
from styles.base import (
    convert_markdown_to_html,
    parse_markdown_file,
    split_content_by_separator,
)

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Missing dependency: playwright")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1440
MAX_HEIGHT = 4320


async def render_html_to_image(
    html_content: str,
    output_path: str,
    width: int,
    height: int,
    max_height: int,
    dpr: int,
    page,
) -> int:
    """Render HTML to PNG using an existing Playwright page. Returns actual height."""
    await page.set_content(html_content, wait_until="load")
    await page.evaluate("() => document.fonts.ready")

    # Let content determine height (within bounds)
    content_height = await page.evaluate(
        """() => {
        const el = document.querySelector('.page');
        return el ? el.scrollHeight : document.body.scrollHeight;
    }"""
    )
    actual_height = max(height, min(content_height, max_height))

    await page.screenshot(
        path=output_path,
        clip={"x": 0, "y": 0, "width": width, "height": actual_height},
        type="png",
    )
    print(f"  -> {output_path} ({width}x{actual_height})")
    return actual_height


async def render(
    md_file: str,
    output_dir: str,
    style_name: str,
    width: int,
    height: int,
    max_height: int,
    dpr: int,
):
    style = get_style(style_name)
    print(f"Rendering: {md_file}")
    print(f"Style: {style.STYLE_NAME} — {style.STYLE_DESCRIPTION}")

    os.makedirs(output_dir, exist_ok=True)

    data = parse_markdown_file(md_file)
    metadata = data["metadata"]
    body = data["body"]

    sections = split_content_by_separator(body)
    if not sections:
        print("No content found.")
        return

    title = metadata.get("title", "")
    subtitle = metadata.get("subtitle", "")

    # First section → cover, rest → cards
    first_section_html = convert_markdown_to_html(sections[0])
    card_sections = sections[1:]
    total_pages = 1 + len(card_sections)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": max_height},
            device_scale_factor=dpr,
        )

        # Page 1: cover
        cover_html = style.generate_cover(
            title, subtitle, first_section_html, width, height
        )
        await render_html_to_image(
            cover_html,
            os.path.join(output_dir, "page_1.png"),
            width, height, max_height, dpr, page,
        )

        # Page 2+: cards
        for i, section in enumerate(card_sections, start=2):
            section_html = convert_markdown_to_html(section)
            card_html = style.generate_card(
                section_html, i, total_pages, width, height
            )
            await render_html_to_image(
                card_html,
                os.path.join(output_dir, f"page_{i}.png"),
                width, height, max_height, dpr, page,
            )

        await page.close()
        await browser.close()

    print(f"\nDone! {total_pages} pages saved to {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Render markdown to styled image cards"
    )
    parser.add_argument("markdown_file", help="Markdown file path")
    parser.add_argument(
        "--style", "-s", required=True,
        choices=list_styles(),
        help="Visual style",
    )
    parser.add_argument(
        "--output-dir", "-o", default=os.getcwd(),
        help="Output directory (default: cwd)",
    )
    parser.add_argument("--width", "-w", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--max-height", type=int, default=MAX_HEIGHT)
    parser.add_argument("--dpr", type=int, default=2)

    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print(f"File not found: {args.markdown_file}")
        sys.exit(1)

    asyncio.run(
        render(
            args.markdown_file,
            args.output_dir,
            style_name=args.style,
            width=args.width,
            height=args.height,
            max_height=args.max_height,
            dpr=args.dpr,
        )
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify CLI help works**

Run: `cd /Users/linguanguo/dev/Auto-Redbook-Skills && python scripts/render.py --help`
Expected: shows usage with `--style` as required argument

- [ ] **Step 3: Commit**

```bash
git add scripts/render.py
git commit -m "feat: add render.py — new style-based rendering entry point"
```

---

### Task 5: Prepare the Python Blog Post for Rendering

**Files:**
- Create: a rendering-ready markdown file (location to be determined by user, e.g. in output dir)

This is the AI-assisted preparation step: take the original blog post, add YAML frontmatter and `---` page separators at logical break points. Every word of the original is preserved.

- [ ] **Step 1: Read the original blog post and create the rendering-ready version**

Read `/Users/linguanguo/dev/CyberMnema/timeline/2026/03/W13/blog-python-type-discoveries-2026-03-26.md` and create a new file with:
- YAML frontmatter: `title` and `subtitle` extracted from the original
- `---` separators inserted at logical page breaks (roughly one "discovery" per page)
- All original text preserved verbatim

- [ ] **Step 2: Verify the file parses correctly**

Run: `cd /Users/linguanguo/dev/Auto-Redbook-Skills && python -c "import sys; sys.path.insert(0, 'scripts'); from styles.base import parse_markdown_file, split_content_by_separator; d = parse_markdown_file('<path_to_file>'); print(f'Title: {d[\"metadata\"].get(\"title\", \"\")}'); sections = split_content_by_separator(d['body']); print(f'Sections: {len(sections)}')"`

Expected: shows title and section count

---

### Task 6: End-to-End Render Test

- [ ] **Step 1: Run the renderer on the prepared blog post**

Run: `cd /Users/linguanguo/dev/Auto-Redbook-Skills && python scripts/render.py <prepared_file> --style paper -o ./output/paper-test`

Expected: generates `page_1.png`, `page_2.png`, ... in `output/paper-test/`

- [ ] **Step 2: Visually verify the output**

Open the generated PNGs and check:
- Paper texture background (warm #f4f0e8)
- Horizontal ruled lines visible
- Left red margin line visible
- Page 1 has large title + first section content
- Subsequent pages have section content
- Font size comfortable for phone reading
- Page numbers in bottom right

- [ ] **Step 3: Iterate on styling if needed**

Adjust CSS values in `scripts/styles/paper.py` based on visual feedback. Re-render until satisfied.

- [ ] **Step 4: Commit final version**

```bash
git add -A scripts/styles/ scripts/render.py
git commit -m "feat: style system with paper style — end-to-end working"
```

---

### Task 7: Update README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add new section to README describing the new style system**

Add a section (separate from old theme documentation) covering:
- What the new style system is
- Usage: `python scripts/render.py input.md --style paper -o ./output`
- Available styles (paper)
- How to prepare input markdown (YAML frontmatter + `---` separators)
- How to add new styles (create a module in `scripts/styles/`)

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add new style system documentation to README"
```
