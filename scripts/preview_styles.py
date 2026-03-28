#!/usr/bin/env python3
"""
Generate an HTML preview page showing all available styles side by side.

Usage:
    python scripts/preview_styles.py [-o preview.html]
    python scripts/preview_styles.py  # opens in browser directly
"""

import argparse
import html
import os
import sys
import tempfile
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from styles import get_style, list_styles
from styles.base import convert_markdown_to_html, title_font_size

SAMPLE_TITLE = "示例文章标题"
SAMPLE_SUBTITLE = "这是一个风格预览"
SAMPLE_CONTENT = """\
这是正文第一段。用来展示普通段落的排版效果，包括字号、行高、颜色和间距。

## 二级标题

段落中会有**加粗文字**和*斜体文字*，以及 `行内代码` 的展示。

- 列表项一：展示列表样式
- 列表项二：包含 `code` 的列表
- 列表项三：最后一项

> 这是一段引用文字，用来展示 blockquote 的样式效果。

```python
class Example(BaseModel):
    name: str
    value: int = 0
```

普通段落收尾，展示段落间距。
"""


def generate_preview_html(output_path: str = None):
    styles = list_styles()
    sample_html = convert_markdown_to_html(SAMPLE_CONTENT)

    cards = []
    for name in styles:
        style = get_style(name)

        cover_html = style.generate_cover(
            SAMPLE_TITLE, SAMPLE_SUBTITLE, sample_html,
            width=1080, height=1440,
        )
        card_html = style.generate_card(
            sample_html, 2, 3,
            width=1080, height=1440,
        )

        # Escape for srcdoc
        cover_escaped = html.escape(cover_html, quote=True)
        card_escaped = html.escape(card_html, quote=True)

        cards.append(f"""
        <div class="style-card">
            <div class="style-header">
                <h2>{style.STYLE_NAME}</h2>
                <p>{style.STYLE_DESCRIPTION}</p>
            </div>
            <div class="previews">
                <div class="preview-item">
                    <div class="label">Cover</div>
                    <iframe srcdoc="{cover_escaped}" scrolling="no"></iframe>
                </div>
                <div class="preview-item">
                    <div class="label">Card</div>
                    <iframe srcdoc="{card_escaped}" scrolling="no"></iframe>
                </div>
            </div>
        </div>
        """)

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Style Preview</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, 'Helvetica Neue', sans-serif;
    background: #f5f5f5;
    padding: 40px;
}}
h1 {{
    font-size: 28px;
    color: #333;
    margin-bottom: 8px;
}}
.subtitle {{
    font-size: 14px;
    color: #888;
    margin-bottom: 40px;
}}
.style-card {{
    background: #fff;
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 40px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.style-header h2 {{
    font-size: 22px;
    color: #333;
    margin-bottom: 4px;
}}
.style-header p {{
    font-size: 14px;
    color: #888;
    margin-bottom: 20px;
}}
.previews {{
    display: flex;
    gap: 24px;
    overflow-x: auto;
}}
.preview-item {{
    flex-shrink: 0;
}}
.label {{
    font-size: 12px;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}}
iframe {{
    width: 360px;
    height: 480px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    transform-origin: top left;
    overflow: hidden;
}}
</style>
</head>
<body>
<h1>Style Preview</h1>
<p class="subtitle">{len(styles)} styles available. Each shows a cover page and a content card at 1/3 scale.</p>

{"".join(cards)}

<script>
// Scale iframe content to fit the small preview
document.querySelectorAll('iframe').forEach(iframe => {{
    iframe.addEventListener('load', () => {{
        try {{
            const doc = iframe.contentDocument;
            const body = doc.body;
            body.style.transformOrigin = 'top left';
            body.style.transform = 'scale(0.333)';
            body.style.width = '1080px';
            body.style.overflow = 'hidden';
        }} catch(e) {{}}
    }});
}});
</script>
</body>
</html>"""

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page)
        print(f"Preview saved to {output_path}")
        return output_path
    else:
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8")
        tmp.write(page)
        tmp.close()
        print(f"Preview saved to {tmp.name}")
        return tmp.name


def main():
    parser = argparse.ArgumentParser(description="Preview all available styles")
    parser.add_argument("--output", "-o", help="Output HTML path (default: open in browser)")
    args = parser.parse_args()

    path = generate_preview_html(args.output)
    if not args.output:
        webbrowser.open(f"file://{path}")


if __name__ == "__main__":
    main()
