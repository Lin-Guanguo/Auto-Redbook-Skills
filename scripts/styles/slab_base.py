"""Slab base — shared parameterized template for slab style variants."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

# Original slab palette
PALETTE_ORIGINAL = {
    "primary": "#14532d",
    "primary_deep": "#166534",
    "secondary": "#9a3412",
    "page_bg": "#faf8f2",
    "neutral": "#d6d3cd",
    "body_text": "#44403c",
    "strong_text": "#292524",
    "highlight": "#fef3c7",
    "code_bg": "#ecfdf5",
    "code_text": "#065f46",
    "code_block_bg": "#1c1917",
    "code_block_text": "#e7e5e4",
    "muted": "#a8a29e",
    "pipe_bg": "#f0ece4",
}

# Variant A: 靛蓝 + 琥珀
PALETTE_A = {
    "primary": "#1e3a5f",
    "primary_deep": "#1e40af",
    "secondary": "#b45309",
    "page_bg": "#faf8f2",
    "neutral": "#d6d3cd",
    "body_text": "#44403c",
    "strong_text": "#292524",
    "highlight": "#fef3c7",
    "code_bg": "#eff6ff",
    "code_text": "#1e3a8a",
    "code_block_bg": "#1c1917",
    "code_block_text": "#e7e5e4",
    "muted": "#a8a29e",
    "pipe_bg": "#eef2f7",
}

# Variant B: 墨青 + 赤陶
PALETTE_B = {
    "primary": "#134e4a",
    "primary_deep": "#115e59",
    "secondary": "#9a3412",
    "page_bg": "#faf8f2",
    "neutral": "#d6d3cd",
    "body_text": "#44403c",
    "strong_text": "#292524",
    "highlight": "#fef3c7",
    "code_bg": "#f0fdfa",
    "code_text": "#115e59",
    "code_block_bg": "#1c1917",
    "code_block_text": "#e7e5e4",
    "muted": "#a8a29e",
    "pipe_bg": "#f0ece4",
}

# Variant C: 烟墨 + 赭铜
PALETTE_C = {
    "primary": "#334155",
    "primary_deep": "#475569",
    "secondary": "#92400e",
    "page_bg": "#faf8f2",
    "neutral": "#d6d3cd",
    "body_text": "#44403c",
    "strong_text": "#292524",
    "highlight": "#fff7ed",
    "code_bg": "#f8fafc",
    "code_text": "#334155",
    "code_block_bg": "#1c1917",
    "code_block_text": "#e7e5e4",
    "muted": "#a8a29e",
    "pipe_bg": "#f1f5f9",
}


def slab_css(p: dict, width: int, height: int) -> str:
    pad_x = int(width * 0.06)
    pad_top = int(height * 0.04)

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
    background: {p["page_bg"]};
    position: relative;
    padding: {pad_top}px {pad_x}px;
}}

/* Cover page — same background as content pages */
.cover-page {{
    background: {p["page_bg"]};
    padding-top: {int(height * 0.07)}px;
}}

.cover-title-block {{
    margin-bottom: 35px;
}}

.cover-title-block .cover-title {{
    font-weight: 900;
    color: #ffffff;
    line-height: 1.35;
    background: {p["secondary"]};
    display: inline;
    padding: 6px 14px;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}}

.cover-subtitle-block {{
    margin-bottom: 45px;
}}

.cover-subtitle-block .cover-subtitle {{
    font-size: 48px;
    color: {p["primary"]};
    line-height: 1.6;
    font-weight: 600;
    background: {p["neutral"]};
    display: inline;
    padding: 4px 12px;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}}

.cover-body {{
    color: {p["body_text"]};
    font-size: 38px;
    line-height: 1.75;
}}

.cover-body strong {{
    font-weight: 700;
    color: {p["strong_text"]};
    background: {p["highlight"]};
    padding: 2px 6px;
}}

.cover-body em {{
    font-style: italic;
    color: {p["secondary"]};
}}

.cover-body blockquote {{
    border: none;
    padding: 0;
    margin: 0;
    background: transparent;
    color: {p["body_text"]};
    font-size: 38px;
}}

.cover-body blockquote p {{
    margin: 0 0 24px 0;
}}

.cover-series {{
    position: absolute;
    bottom: {int(height * 0.035)}px;
    left: {pad_x}px;
    font-size: 26px;
    color: {p["muted"]};
    letter-spacing: 1px;
}}

/* Content typography */
.content {{
    color: {p["body_text"]};
    font-size: 36px;
    line-height: 1.7;
}}

.content h1 {{
    font-size: 58px;
    font-weight: 900;
    color: #ffffff;
    background: {p["primary"]};
    margin: 0 -{pad_x}px 30px;
    padding: 28px {pad_x}px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 44px;
    font-weight: 800;
    color: #ffffff;
    background: {p["secondary"]};
    margin: 35px -{pad_x}px 24px;
    padding: 22px {pad_x}px;
    line-height: 1.35;
}}

.content h3 {{
    font-size: 38px;
    font-weight: 700;
    color: {p["primary"]};
    margin: 30px 0 16px 0;
    padding: 12px 20px;
    background: {p["neutral"]};
    display: inline-block;
}}

.content p {{ margin-bottom: 26px; }}

.content strong {{
    font-weight: 700;
    color: {p["strong_text"]};
    background: {p["highlight"]};
    padding: 2px 6px;
}}

.content em {{
    font-style: italic;
    color: {p["secondary"]};
}}

.content a {{
    color: {p["secondary"]};
    text-decoration: none;
    border-bottom: 2px solid {p["secondary"]};
}}

.content ul, .content ol {{ margin: 22px 0; padding-left: 44px; }}
.content li {{ margin-bottom: 12px; line-height: 1.6; }}
.content li::marker {{ color: {p["secondary"]}; font-weight: 700; }}

.content blockquote {{
    border: none;
    padding: 24px 30px;
    color: #ffffff;
    background: {p["primary_deep"]};
    margin: 30px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    font-size: 34px;
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    background: {p["code_bg"]};
    padding: 4px 10px;
    border-radius: 5px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 30px;
    color: {p["code_text"]};
}}

.content pre {{
    background: {p["code_block_bg"]};
    color: {p["code_block_text"]};
    padding: 30px;
    margin: 26px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    white-space: pre;
    overflow: hidden;
    font-size: 24px;
    line-height: 1.45;
}}
.content pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: inherit;
}}

/* Tables */
.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 26px 0;
    font-size: 28px;
    line-height: 1.45;
    table-layout: fixed;
    word-break: break-word;
}}

.content thead th {{
    background: {p["secondary"]};
    color: #ffffff;
    font-weight: 700;
    padding: 12px 12px;
    text-align: left;
    font-size: 26px;
}}

.content tbody td {{
    padding: 11px 12px;
    border-bottom: 1px solid {p["neutral"]};
    vertical-align: top;
}}

.content tbody tr:nth-child(odd) td {{
    background: rgba(0,0,0,0.02);
}}

.content tbody tr:last-child td {{
    border-bottom: 3px solid {p["secondary"]};
}}

/* Compact tables: 5+ columns get even smaller text */
.content table.compact {{
    font-size: 24px;
}}
.content table.compact thead th {{
    font-size: 22px;
    padding: 10px 8px;
}}
.content table.compact tbody td {{
    padding: 8px 8px;
}}

.content td code, .content th code {{
    font-size: 22px;
    padding: 2px 6px;
    background: rgba(255,255,255,0.5);
    color: {p["code_text"]};
}}

/* Pipeline diagrams */
.pipeline {{
    margin: 24px 0;
    padding: 0;
}}

.pipe-step {{
    background: {p["pipe_bg"]};
    border-left: 4px solid {p["primary"]};
    padding: 10px 16px;
    font-size: 28px;
    line-height: 1.45;
    color: {p["body_text"]};
}}

.pipe-step.pipe-parallel {{
    background: {p["primary"]};
    color: #ffffff;
    border-left: 4px solid {p["secondary"]};
    font-weight: 600;
}}

.pipe-arrow {{
    text-align: center;
    font-size: 20px;
    line-height: 1;
    color: {p["secondary"]};
    padding: 3px 0;
}}

.content hr {{ border: none; height: 3px; background: {p["neutral"]}; margin: 40px 0; }}

.content img {{
    max-width: 100%;
    height: auto;
    margin: 26px auto;
    display: block;
}}

.page-number {{
    position: absolute;
    bottom: {int(height * 0.03)}px;
    right: {pad_x}px;
    font-size: 28px;
    color: {p["muted"]};
}}
"""


TABLE_COMPACT_JS = """
document.querySelectorAll('.content table').forEach(t => {
    const cols = t.querySelector('tr') ? t.querySelector('tr').children.length : 0;
    if (cols >= 5) t.classList.add('compact');
});
"""


def slab_generate_cover(
    palette, title, subtitle, first_section_html, width, height,
    series_text="",
):
    import re as _re
    clean_title = _re.sub(r'<[^>]+>', '', title)
    t_size = title_font_size(clean_title, width)
    if '<br' not in title:
        t_size = int(t_size * 1.15)
    css = slab_css(palette, width, height)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div class="cover-subtitle-block">
            <div class="cover-subtitle">{subtitle}</div>
        </div>"""

    series_html = ""
    if series_text:
        series_html = f'<div class="cover-series">{series_text}</div>'

    body = f"""
    <div class="page cover-page">
        <div class="cover-title-block">
            <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
        </div>
        {subtitle_html}
        <div class="cover-body">{first_section_html}</div>
        {series_html}
    </div>"""
    return html_document(body, css, width, scripts=TABLE_COMPACT_JS)


def slab_generate_card(palette, content_html, page_number, total_pages, width, height):
    css = slab_css(palette, width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width, scripts=TABLE_COMPACT_JS)
