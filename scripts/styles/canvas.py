"""Canvas style — 画布风格: cream linen background, minimal, quiet."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

STYLE_NAME = "canvas"
STYLE_DESCRIPTION = "画布 — 奶白亚麻底，克制留白，思考型排版"


def _canvas_css(width: int, height: int) -> str:
    pad_x = int(width * 0.09)
    pad_top = int(height * 0.07)

    return f"""
{css_reset()}
{font_imports(["Noto Serif SC", "Noto Sans SC"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
    width: {width}px;
    overflow: hidden;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: #f7f3ed;
    position: relative;
    padding: {pad_top}px {pad_x}px;
    /* Subtle linen texture */
    background-image:
        repeating-linear-gradient(
            45deg,
            transparent,
            transparent 2px,
            rgba(0,0,0,0.008) 2px,
            rgba(0,0,0,0.008) 4px
        );
}}

.cover-title {{
    font-family: 'Noto Serif SC', 'Noto Sans SC', serif;
    font-weight: 700;
    color: #3d2b1f;
    line-height: 1.3;
    margin-bottom: 20px;
}}

.cover-subtitle {{
    font-size: 36px;
    color: #a08060;
    margin-bottom: 60px;
    line-height: 1.5;
}}

.cover-divider {{
    width: 40px;
    height: 40px;
    margin-bottom: 50px;
    border: 2px solid #c0a080;
    border-radius: 50%;
}}

.content {{
    color: #4a3728;
    font-size: 42px;
    line-height: 1.85;
}}

.content h1 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 66px;
    font-weight: 700;
    color: #3d2b1f;
    margin-bottom: 40px;
    line-height: 1.3;
}}

.content h2 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 52px;
    font-weight: 700;
    color: #3d2b1f;
    margin: 55px 0 25px 0;
    line-height: 1.4;
}}

.content h3 {{
    font-size: 46px;
    font-weight: 600;
    color: #5a4030;
    margin: 40px 0 20px 0;
}}

.content p {{ margin-bottom: 38px; }}

.content strong {{
    font-weight: 700;
    color: #3d2b1f;
}}

.content em {{
    font-style: italic;
    color: #8a6040;
}}

.content ul, .content ol {{ margin: 30px 0; padding-left: 50px; }}
.content li {{ margin-bottom: 20px; line-height: 1.7; }}
.content li::marker {{ color: #c0a080; }}

.content blockquote {{
    border-left: 4px solid #c0a080;
    padding: 25px 30px;
    color: #7a6050;
    font-style: italic;
    margin: 40px 0;
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    background: rgba(0,0,0,0.05);
    padding: 6px 14px;
    border-radius: 6px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 36px;
    color: #5a4030;
}}

.content pre {{
    background: #3d2b1f;
    color: #e8ddd0;
    padding: 40px;
    border-radius: 10px;
    margin: 40px 0;
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

.content hr {{ border: none; height: 1px; background: #d0c0a8; margin: 55px 0; }}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.04)}px;
    right: {pad_x}px;
    font-size: 32px;
    color: #c0a080;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = title_font_size(title, width)
    css = _canvas_css(width, height)
    pad_top = int(height * 0.08)
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
    css = _canvas_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
