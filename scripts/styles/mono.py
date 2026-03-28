"""Mono style — 等宽打字机风格: monospace font, typewriter aesthetic."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

STYLE_NAME = "mono"
STYLE_DESCRIPTION = "等宽打字机 — 全等宽字体，技术文档感"


def _mono_css(width: int, height: int) -> str:
    pad_x = int(width * 0.08)
    pad_top = int(height * 0.06)

    return f"""
{css_reset()}
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@300;400;500;700&display=swap');
{font_imports(["Noto Sans SC"])}

body {{
    font-family: 'Noto Sans Mono', 'SF Mono', 'Consolas', monospace;
    width: {width}px;
    overflow: hidden;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: #f0f0f0;
    position: relative;
    padding: {pad_top}px {pad_x}px;
}}

.cover-title {{
    font-weight: 400;
    color: #1a1a1a;
    line-height: 1.3;
    margin-bottom: 20px;
    letter-spacing: -1px;
}}

.cover-subtitle {{
    font-size: 34px;
    color: #888;
    margin-bottom: 50px;
    line-height: 1.5;
}}

.cover-divider {{
    width: 100%;
    height: 2px;
    background: #1a1a1a;
    margin-bottom: 45px;
}}

.content {{
    font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
    color: #333;
    font-size: 42px;
    line-height: 1.8;
}}

.content h1, .content h2, .content h3 {{
    font-family: 'Noto Sans Mono', 'SF Mono', monospace;
    font-weight: 400;
    color: #1a1a1a;
}}

.content h1 {{
    font-size: 64px;
    margin-bottom: 40px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 50px;
    margin: 50px 0 25px 0;
    line-height: 1.4;
    padding-bottom: 15px;
    border-bottom: 2px solid #1a1a1a;
}}

.content h3 {{
    font-size: 44px;
    margin: 40px 0 20px 0;
}}

.content p {{ margin-bottom: 35px; }}

.content strong {{
    font-weight: 700;
    color: #1a1a1a;
    background: #e8e8e8;
    padding: 2px 8px;
}}

.content em {{
    font-style: italic;
    color: #555;
}}

.content ul, .content ol {{ margin: 30px 0; padding-left: 50px; }}
.content li {{ margin-bottom: 18px; line-height: 1.7; }}

.content blockquote {{
    border-left: 3px solid #1a1a1a;
    padding: 20px 30px;
    color: #666;
    margin: 35px 0;
    background: #e8e8e8;
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    font-family: 'Noto Sans Mono', monospace;
    font-size: 36px;
    color: #333;
    background: #e0e0e0;
    padding: 4px 12px;
    border-radius: 4px;
}}

.content pre {{
    background: #1a1a1a;
    color: #d4d4d4;
    padding: 40px;
    margin: 35px 0;
    border-radius: 0;
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

.content hr {{ border: none; height: 2px; background: #1a1a1a; margin: 50px 0; }}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.04)}px;
    right: {pad_x}px;
    font-size: 30px;
    color: #999;
    font-family: 'Noto Sans Mono', monospace;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = title_font_size(title, width)
    css = _mono_css(width, height)
    pad_top = int(height * 0.06)
    subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>' if subtitle else ""
    body = f"""
    <div class="page">
        <div class="cover-title" style="font-size: {t_size}px; padding-top: {pad_top}px;">{title}</div>
        {subtitle_html}
        <div class="cover-divider"></div>
        <div class="content">{first_section_html}</div>
    </div>"""
    return html_document(body, css, width)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _mono_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
