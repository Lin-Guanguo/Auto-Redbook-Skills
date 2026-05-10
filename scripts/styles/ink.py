"""Ink style — 黑板研究笔记: dark charcoal bg, electric cyan headings, amber highlights."""

from styles.base import (
    css_reset,
    font_imports,
    html_document,
    page_number_html,
    title_font_size,
)

STYLE_NAME = "ink"
STYLE_DESCRIPTION = "黑板研究笔记 — 深炭黑底 + 青蓝标题 + 琥珀高亮"

BG = "#1a1c20"
BG2 = "#22252b"
TEXT = "#e8e6e0"
MUTED = "#8a8a8a"
CYAN = "#4ecdc4"
AMBER = "#f7b731"
ACCENT = "#4ecdc4"


def _ink_css(width: int, height: int) -> str:
    pad_x = int(width * 0.072)
    pad_y = int(height * 0.05)

    return f"""
{css_reset()}
{font_imports(["Noto Sans SC", "Noto Serif SC", "Space Mono"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
    width: {width}px;
    overflow: hidden;
    background: transparent;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: {BG};
    position: relative;
    padding: {pad_y}px {pad_x}px {pad_y}px {pad_x}px;
    box-sizing: border-box;
}}

/* ===== Cover ===== */
.cover-tag {{
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 26px;
    color: {CYAN};
    border: 1.5px solid {CYAN};
    padding: 6px 18px;
    border-radius: 2px;
    letter-spacing: 0.1em;
    margin-bottom: 48px;
}}

.cover-title {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-weight: 900;
    color: {TEXT};
    line-height: 1.3;
    margin-bottom: 16px;
}}

.cover-subtitle {{
    font-size: 42px;
    font-weight: 700;
    color: {CYAN};
    line-height: 1.5;
    margin-bottom: 56px;
}}

.cover-rule {{
    height: 1px;
    background: linear-gradient(90deg, {CYAN}, transparent);
    margin-bottom: 52px;
}}

/* ===== Content typography ===== */
.content {{
    color: {TEXT};
    font-size: 34px;
    line-height: 1.75;
    font-weight: 400;
}}

.content h1 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 60px;
    font-weight: 900;
    color: {CYAN};
    margin-bottom: 36px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 46px;
    font-weight: 700;
    color: {CYAN};
    margin: 56px 0 24px 0;
    line-height: 1.35;
    padding-left: 20px;
    border-left: 4px solid {CYAN};
}}

.content h3 {{
    font-size: 40px;
    font-weight: 700;
    color: {AMBER};
    margin: 40px 0 18px 0;
    line-height: 1.4;
}}

.content p {{
    margin-bottom: 26px;
}}

.content strong {{
    font-weight: 700;
    color: {BG};
    background: {AMBER};
    padding: 1px 6px;
    border-radius: 2px;
}}

.content em {{
    font-style: italic;
    color: {CYAN};
}}

.content a {{
    color: {CYAN};
    text-decoration: none;
    border-bottom: 1px solid rgba(78,205,196,0.4);
}}

.content ul, .content ol {{
    margin: 22px 0;
    padding-left: 48px;
}}

.content li {{
    margin-bottom: 14px;
    line-height: 1.65;
}}

.content li::marker {{
    color: {CYAN};
}}

/* ===== Blockquote ===== */
.content blockquote {{
    background: {BG2};
    border-left: 4px solid {AMBER};
    padding: 40px 42px;
    margin: 44px 0;
    border-radius: 0 4px 4px 0;
}}

.content blockquote p {{
    font-family: 'Noto Serif SC', serif;
    font-size: 38px;
    line-height: 1.6;
    color: {AMBER};
    margin: 0;
    font-style: italic;
}}

.content blockquote strong {{
    background: none;
    color: {AMBER};
    font-weight: 700;
    padding: 0;
}}

/* ===== Code ===== */
.content code {{
    background: rgba(78,205,196,0.12);
    color: {CYAN};
    padding: 3px 10px;
    border-radius: 3px;
    font-family: 'Space Mono', 'SF Mono', monospace;
    font-size: 30px;
}}

.content pre {{
    background: #0d0f12;
    border: 1px solid rgba(78,205,196,0.2);
    padding: 38px;
    border-radius: 6px;
    margin: 32px 0;
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    font-size: 26px;
    line-height: 1.6;
}}

.content pre code {{
    background: transparent;
    color: {TEXT};
    padding: 0;
    font-size: inherit;
}}

.content hr {{
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 50px 0;
}}

/* ===== Tables ===== */
.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 32px 0;
    font-size: 30px;
}}

.content th, .content td {{
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 18px 14px;
    text-align: left;
    line-height: 1.5;
    vertical-align: top;
}}

.content th {{
    color: {CYAN};
    font-weight: 700;
    border-bottom: 2px solid {CYAN};
    font-size: 28px;
    letter-spacing: 0.04em;
}}

.content tr:nth-child(even) td {{
    background: rgba(255,255,255,0.03);
}}

/* ===== Page number ===== */
.page-number {{
    position: absolute;
    bottom: {int(height * 0.033)}px;
    right: {pad_x}px;
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    color: {MUTED};
    letter-spacing: 0.06em;
}}

/* ===== Corner accent ===== */
.corner-dot {{
    position: absolute;
    top: 40px;
    right: {pad_x}px;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: {CYAN};
}}
"""


def generate_cover(
    title: str,
    subtitle: str,
    first_section_html: str,
    width: int,
    height: int,
) -> str:
    pad_x = int(width * 0.072)
    avail = width - 2 * pad_x
    # Compute em-width: CJK/fullwidth=1.0, ASCII=0.56
    em = sum(1.0 if ord(c) > 0x2E7F else 0.56 for c in title)
    t_size = int(avail * 0.95 / em) if em else title_font_size(title, width)
    css = _ink_css(width, height)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>'

    body = f"""
    <div class="page">
        <div class="cover-tag">RESEARCH · AI</div>
        <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
        {subtitle_html}
        <div class="cover-rule"></div>
        <div class="content">{first_section_html}</div>
        <div class="corner-dot"></div>
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
    css = _ink_css(width, height)
    page_num = page_number_html(page_number, total_pages)

    body = f"""
    <div class="page">
        <div class="corner-dot"></div>
        <div class="content">{content_html}</div>
        {page_num}
    </div>
    """
    return html_document(body, css, width)
