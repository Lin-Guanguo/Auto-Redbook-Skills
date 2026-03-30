"""Slab style — 厚板风: warm color blocks, forest green + terracotta editorial."""

from styles.base import css_reset, font_imports, html_document, page_number_html, title_font_size

STYLE_NAME = "slab"
STYLE_DESCRIPTION = "厚板 — 暖色大色块，森绿+赤陶，杂志编辑感"
COVER_HEIGHT = 1440


def _slab_css(width: int, height: int) -> str:
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
    background: #faf8f2;
    position: relative;
    padding: {pad_top}px {pad_x}px;
}}

/* Cover page — same background as content pages */
.cover-page {{
    background: #faf8f2;
    padding-top: {int(height * 0.07)}px;
}}

.cover-title-block {{
    margin-bottom: 35px;
}}

.cover-title-block .cover-title {{
    font-weight: 900;
    color: #ffffff;
    line-height: 1.35;
    background: #9a3412;
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
    color: #14532d;
    line-height: 1.6;
    font-weight: 600;
    background: #d6d3cd;
    display: inline;
    padding: 4px 12px;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}}

.cover-body {{
    color: #44403c;
    font-size: 38px;
    line-height: 1.75;
}}

.cover-body strong {{
    font-weight: 700;
    color: #292524;
    background: #fef3c7;
    padding: 2px 6px;
}}

.cover-body em {{
    font-style: italic;
    color: #9a3412;
}}

.cover-body blockquote {{
    border: none;
    padding: 0;
    margin: 0;
    background: transparent;
    color: #44403c;
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
    color: #a8a29e;
    letter-spacing: 1px;
}}

/* Content typography */
.content {{
    color: #44403c;
    font-size: 36px;
    line-height: 1.7;
}}

.content h1 {{
    font-size: 58px;
    font-weight: 900;
    color: #ffffff;
    background: #14532d;
    margin: 0 -{pad_x}px 30px;
    padding: 28px {pad_x}px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 44px;
    font-weight: 800;
    color: #ffffff;
    background: #9a3412;
    margin: 35px -{pad_x}px 24px;
    padding: 22px {pad_x}px;
    line-height: 1.35;
}}

.content h3 {{
    font-size: 38px;
    font-weight: 700;
    color: #14532d;
    margin: 30px 0 16px 0;
    padding: 12px 20px;
    background: #d6d3cd;
    display: inline-block;
}}

.content p {{ margin-bottom: 26px; }}

.content strong {{
    font-weight: 700;
    color: #292524;
    background: #fef3c7;
    padding: 2px 6px;
}}

.content em {{
    font-style: italic;
    color: #9a3412;
}}

.content a {{
    color: #9a3412;
    text-decoration: none;
    border-bottom: 2px solid #9a3412;
}}

.content ul, .content ol {{ margin: 22px 0; padding-left: 44px; }}
.content li {{ margin-bottom: 12px; line-height: 1.6; }}
.content li::marker {{ color: #9a3412; font-weight: 700; }}

.content blockquote {{
    border: none;
    padding: 24px 30px;
    color: #ffffff;
    background: #166534;
    margin: 30px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    font-size: 34px;
}}
.content blockquote p {{ margin: 0; }}

.content code {{
    background: #ecfdf5;
    padding: 4px 10px;
    border-radius: 5px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 30px;
    color: #065f46;
}}

.content pre {{
    background: #1c1917;
    color: #e7e5e4;
    padding: 30px;
    margin: 26px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
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
    background: #9a3412;
    color: #ffffff;
    font-weight: 700;
    padding: 12px 12px;
    text-align: left;
    font-size: 26px;
}}

.content tbody td {{
    padding: 11px 12px;
    border-bottom: 1px solid #d6d3cd;
    vertical-align: top;
}}

.content tbody tr:nth-child(odd) td {{
    background: rgba(0,0,0,0.02);
}}

.content tbody tr:last-child td {{
    border-bottom: 3px solid #9a3412;
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
    color: #065f46;
}}

/* Pipeline diagrams */
.pipeline {{
    margin: 24px 0;
    padding: 0;
}}

.pipe-step {{
    background: #f0ece4;
    border-left: 4px solid #14532d;
    padding: 10px 16px;
    font-size: 28px;
    line-height: 1.45;
    color: #44403c;
}}

.pipe-step.pipe-parallel {{
    background: #14532d;
    color: #ffffff;
    border-left: 4px solid #9a3412;
    font-weight: 600;
}}

.pipe-arrow {{
    text-align: center;
    font-size: 20px;
    line-height: 1;
    color: #9a3412;
    padding: 3px 0;
}}

.content hr {{ border: none; height: 3px; background: #d6d3cd; margin: 40px 0; }}

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
    color: #a8a29e;
}}
"""


_TABLE_COMPACT_JS = """
document.querySelectorAll('.content table').forEach(t => {
    const cols = t.querySelector('tr') ? t.querySelector('tr').children.length : 0;
    if (cols >= 5) t.classList.add('compact');
});
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = title_font_size(title, width)
    # Cover title a bit bigger than default
    t_size = int(t_size * 1.15)
    css = _slab_css(width, height)
    pad_x = int(width * 0.06)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div class="cover-subtitle-block">
            <div class="cover-subtitle">{subtitle}</div>
        </div>"""

    body = f"""
    <div class="page cover-page">
        <div class="cover-title-block">
            <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
        </div>
        {subtitle_html}
        <div class="cover-body">{first_section_html}</div>
        <div class="cover-series">LLM Agent 研究系列 · 第二篇</div>
    </div>"""
    return html_document(body, css, width, scripts=_TABLE_COMPACT_JS)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _slab_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width, scripts=_TABLE_COMPACT_JS)
