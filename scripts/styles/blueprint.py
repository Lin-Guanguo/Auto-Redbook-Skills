"""Blueprint style — 蓝图风格: light blue-gray bg, grid lines, engineering feel."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

STYLE_NAME = "blueprint"
STYLE_DESCRIPTION = "蓝图 — 浅蓝灰底 + 网格线，工程图纸感"


def _blueprint_css(width: int, height: int) -> str:
    pad_x = int(width * 0.07)
    pad_top = int(height * 0.05)
    grid = 30

    return f"""
{css_reset()}
{font_imports(["Noto Sans SC"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
    width: {width}px;
    overflow: hidden;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: #e8edf2;
    position: relative;
    padding: {pad_top}px {pad_x}px;
    background-image:
        linear-gradient(rgba(100,130,170,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(100,130,170,0.08) 1px, transparent 1px);
    background-size: {grid}px {grid}px;
}}

.cover-title {{
    font-weight: 800;
    color: #1e3a5f;
    line-height: 1.25;
    margin-bottom: 20px;
}}

.cover-subtitle {{
    font-size: 36px;
    color: #6b8299;
    margin-bottom: 50px;
    line-height: 1.5;
}}

.cover-divider {{
    width: 60px;
    height: 3px;
    background: #2563eb;
    margin-bottom: 45px;
}}

.content {{
    color: #2d3748;
    font-size: 42px;
    line-height: 1.8;
}}

.content h1 {{
    font-size: 68px;
    font-weight: 800;
    color: #1e3a5f;
    margin-bottom: 40px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 54px;
    font-weight: 700;
    color: #1e3a5f;
    margin: 50px 0 25px 0;
    line-height: 1.4;
    padding-left: 20px;
    border-left: 6px solid #2563eb;
}}

.content h3 {{
    font-size: 46px;
    font-weight: 600;
    color: #2d4a6e;
    margin: 40px 0 20px 0;
}}

.content p {{ margin-bottom: 35px; }}

.content strong {{
    font-weight: 700;
    color: #1e3a5f;
}}

.content em {{
    font-style: italic;
    color: #2563eb;
}}

.content ul, .content ol {{ margin: 30px 0; padding-left: 50px; }}
.content li {{ margin-bottom: 18px; line-height: 1.7; }}
.content li::marker {{ color: #2563eb; }}

.content blockquote {{
    border-left: 4px solid #2563eb;
    padding: 25px 30px;
    color: #4a6280;
    margin: 35px 0;
    background: rgba(37, 99, 235, 0.04);
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    background: rgba(37, 99, 235, 0.08);
    padding: 6px 14px;
    border-radius: 6px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 36px;
    color: #2563eb;
}}

.content pre {{
    background: #1e293b;
    color: #cbd5e1;
    padding: 40px;
    border-radius: 8px;
    margin: 35px 0;
    border: 1px solid rgba(37, 99, 235, 0.15);
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

.content hr {{ border: none; height: 1px; background: rgba(100,130,170,0.2); margin: 50px 0; }}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.04)}px;
    right: {pad_x}px;
    font-size: 32px;
    color: #8ea4b8;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = title_font_size(title, width)
    css = _blueprint_css(width, height)
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
    css = _blueprint_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
