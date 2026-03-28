"""Block style — 色块风格: bold colored blocks for headings, modern editorial."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

STYLE_NAME = "block"
STYLE_DESCRIPTION = "色块 — 大色块标题，现代编辑感，视觉节奏强"


def _block_css(width: int, height: int) -> str:
    pad_x = int(width * 0.06)
    pad_top = int(height * 0.05)

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
    background: #fafafa;
    position: relative;
    padding: {pad_top}px {pad_x}px;
}}

/* Cover: title on a big color block */
.cover-block {{
    background: #1e293b;
    margin: 0 -{pad_x}px;
    padding: {int(height * 0.06)}px {pad_x}px {int(height * 0.04)}px;
    margin-bottom: 45px;
}}

.cover-block .cover-title {{
    font-weight: 900;
    color: #ffffff;
    line-height: 1.25;
    margin-bottom: 16px;
}}

.cover-block .cover-subtitle {{
    font-size: 36px;
    color: rgba(255,255,255,0.6);
    line-height: 1.5;
}}

/* Content typography */
.content {{
    color: #374151;
    font-size: 42px;
    line-height: 1.8;
}}

.content h1 {{
    font-size: 68px;
    font-weight: 900;
    color: #ffffff;
    background: #1e293b;
    margin: 0 -{pad_x}px 40px;
    padding: 35px {pad_x}px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 50px;
    font-weight: 800;
    color: #ffffff;
    background: #4f46e5;
    margin: 45px -{pad_x}px 30px;
    padding: 28px {pad_x}px;
    line-height: 1.35;
}}

.content h3 {{
    font-size: 46px;
    font-weight: 700;
    color: #1e293b;
    margin: 40px 0 20px 0;
    padding: 15px 24px;
    background: #e5e7eb;
    display: inline-block;
}}

.content p {{ margin-bottom: 35px; }}

.content strong {{
    font-weight: 700;
    color: #1e293b;
    background: #fde68a;
    padding: 2px 6px;
}}

.content em {{
    font-style: italic;
    color: #4f46e5;
}}

.content a {{
    color: #4f46e5;
    text-decoration: none;
    border-bottom: 2px solid #4f46e5;
}}

.content ul, .content ol {{ margin: 30px 0; padding-left: 50px; }}
.content li {{ margin-bottom: 18px; line-height: 1.7; }}
.content li::marker {{ color: #4f46e5; font-weight: 700; }}

.content blockquote {{
    border: none;
    padding: 30px 35px;
    color: #ffffff;
    background: #6366f1;
    margin: 40px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    font-size: 40px;
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    background: #eef2ff;
    padding: 6px 14px;
    border-radius: 6px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 36px;
    color: #4338ca;
}}

.content pre {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 40px;
    margin: 35px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
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

.content hr {{ border: none; height: 3px; background: #e5e7eb; margin: 50px 0; }}

.content img {{
    max-width: 100%;
    height: auto;
    margin: 35px auto;
    display: block;
}}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.03)}px;
    right: {pad_x}px;
    font-size: 30px;
    color: #9ca3af;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = title_font_size(title, width)
    css = _block_css(width, height)
    subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>' if subtitle else ""

    body = f"""
    <div class="page">
        <div class="cover-block">
            <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
            {subtitle_html}
        </div>
        <div class="content">{first_section_html}</div>
    </div>"""
    return html_document(body, css, width)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _block_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
