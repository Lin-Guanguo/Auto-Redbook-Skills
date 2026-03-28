"""Kraft style — 牛皮纸风格: brown kraft paper background, earthy, raw."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

STYLE_NAME = "kraft"
STYLE_DESCRIPTION = "牛皮纸 — 棕色纸底，粗犷质朴，手工质感"


def _kraft_css(width: int, height: int) -> str:
    pad_x = int(width * 0.08)
    pad_top = int(height * 0.06)

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
    background: #d4c5a9;
    position: relative;
    padding: {pad_top}px {pad_x}px;
    /* Subtle paper grain */
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 3px,
            rgba(0,0,0,0.015) 3px,
            rgba(0,0,0,0.015) 4px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 5px,
            rgba(0,0,0,0.01) 5px,
            rgba(0,0,0,0.01) 6px
        );
}}

.cover-title {{
    font-weight: 900;
    color: #3b2a1a;
    line-height: 1.25;
    margin-bottom: 20px;
}}

.cover-subtitle {{
    font-size: 36px;
    color: #7a6a55;
    margin-bottom: 50px;
    line-height: 1.5;
}}

.cover-divider {{
    width: 80px;
    height: 4px;
    background: #3b2a1a;
    margin-bottom: 45px;
}}

.content {{
    color: #3b2a1a;
    font-size: 42px;
    line-height: 1.8;
}}

.content h1 {{
    font-size: 68px;
    font-weight: 900;
    color: #2a1a0a;
    margin-bottom: 40px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 54px;
    font-weight: 800;
    color: #2a1a0a;
    margin: 50px 0 25px 0;
    line-height: 1.4;
    text-decoration: underline;
    text-decoration-color: rgba(59, 42, 26, 0.3);
    text-underline-offset: 10px;
    text-decoration-thickness: 3px;
}}

.content h3 {{
    font-size: 46px;
    font-weight: 700;
    color: #3b2a1a;
    margin: 40px 0 20px 0;
}}

.content p {{ margin-bottom: 35px; }}

.content strong {{
    font-weight: 800;
    color: #2a1a0a;
}}

.content em {{
    font-style: italic;
    color: #5a4a35;
}}

.content ul, .content ol {{ margin: 30px 0; padding-left: 50px; }}
.content li {{ margin-bottom: 18px; line-height: 1.7; }}
.content li::marker {{ color: #7a5a3a; }}

.content blockquote {{
    border-left: 5px solid #7a5a3a;
    padding: 25px 30px;
    color: #5a4a35;
    margin: 35px 0;
    background: rgba(0,0,0,0.04);
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    background: rgba(0,0,0,0.08);
    padding: 6px 14px;
    border-radius: 4px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 36px;
    color: #3b2a1a;
}}

.content pre {{
    background: #2a1a0a;
    color: #d4c5a9;
    padding: 40px;
    border-radius: 6px;
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

.content hr {{ border: none; height: 2px; background: rgba(59,42,26,0.2); margin: 50px 0; }}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.04)}px;
    right: {pad_x}px;
    font-size: 32px;
    color: #9a8a70;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = title_font_size(title, width)
    css = _kraft_css(width, height)
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
    css = _kraft_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
