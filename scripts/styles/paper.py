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
    font-size: 28px;
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
