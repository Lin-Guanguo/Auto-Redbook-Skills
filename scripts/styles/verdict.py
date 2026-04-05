"""Verdict style — 裁定书风格: parchment bg, serif titles, clause numbers, red annotations, stamp."""

import re as _re

from styles.base import css_reset, font_imports, html_document, page_number_html


def _inject_clause_prefix(html_content: str) -> str:
    """Add § prefix to h2 headings."""

    def _replace(m):
        attrs = m.group(1) or ""
        inner = m.group(2)
        return f'<h2{attrs}><span class="clause">§</span> {inner}</h2>'

    return _re.sub(r'<h2([^>]*)>(.*?)</h2>', _replace, html_content)

STYLE_NAME = "verdict"
STYLE_DESCRIPTION = "裁定书 — 羊皮纸底，衬线标题，条款编号，朱红批注，「待裁定」印章"
COVER_HEIGHT = 1920


def _verdict_css(width: int, height: int) -> str:
    pad_x = int(width * 0.06)
    pad_top = int(height * 0.05)

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
    background: #f5f0e1;
    position: relative;
    padding: {pad_top}px {pad_x}px;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent, transparent 59px,
            rgba(139,115,85,0.08) 59px, rgba(139,115,85,0.08) 60px
        );
}}

/* Top double rule */
.page::before {{
    content: '';
    position: absolute;
    top: {int(height * 0.03)}px;
    left: {pad_x}px;
    right: {pad_x}px;
    height: 6px;
    border-top: 2px solid #8b7355;
    border-bottom: 1px solid #8b7355;
}}

/* Bottom rule */
.page::after {{
    content: '';
    position: absolute;
    bottom: {int(height * 0.03)}px;
    left: {pad_x}px;
    right: {pad_x}px;
    height: 0;
    border-bottom: 1px solid #8b7355;
}}

/* ---- Cover ---- */
.cover-page {{
    padding-top: {int(height * 0.07)}px;
}}

.cover-title {{
    font-family: 'Noto Serif SC', serif;
    font-weight: 900;
    color: #3d2b1f;
    line-height: 1.3;
    margin-bottom: 36px;
}}

.cover-subtitle {{
    font-size: 42px;
    color: #8b7355;
    line-height: 1.6;
    margin-bottom: 60px;
    padding-bottom: 40px;
    border-bottom: 1px solid rgba(139,115,85,0.3);
}}

.cover-body {{
    color: #5a4a3a;
    font-size: 42px;
    line-height: 1.8;
}}

.cover-body p {{ margin-bottom: 32px; }}

.cover-body strong {{
    color: #b33a2b;
    font-weight: 700;
    border-bottom: 2px solid rgba(179,58,43,0.3);
}}

.cover-body em {{
    font-style: italic;
    color: #8b7355;
}}

.cover-body blockquote {{
    border: none;
    padding: 0;
    margin: 0;
    background: transparent;
    color: #5a4a3a;
    font-size: 42px;
}}

.cover-body blockquote p {{
    margin: 0 0 24px 0;
}}

/* Stamp */
.stamp {{
    position: absolute;
    bottom: {int(height * 0.13)}px;
    right: {int(width * 0.07)}px;
    width: {int(width * 0.30)}px;
    height: {int(width * 0.30)}px;
    border: 8px solid rgba(179,58,43,0.55);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: rotate(-18deg);
    color: rgba(179,58,43,0.55);
    font-family: 'Noto Serif SC', serif;
    font-size: {int(width * 0.052)}px;
    font-weight: 900;
    letter-spacing: 8px;
    text-align: center;
    line-height: 1.3;
}}

.stamp::before {{
    content: '';
    position: absolute;
    inset: 12px;
    border: 3px solid rgba(179,58,43,0.35);
    border-radius: 50%;
}}

.cover-series {{
    position: absolute;
    bottom: {int(height * 0.035)}px;
    left: {pad_x}px;
    font-size: 26px;
    color: #a89880;
    letter-spacing: 1px;
}}

/* ---- Content ---- */
.content {{
    color: #5a4a3a;
    font-size: 42px;
    line-height: 1.8;
}}

.content h1 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 64px;
    font-weight: 900;
    color: #3d2b1f;
    margin-bottom: 36px;
    padding-bottom: 16px;
    border-bottom: 2px solid rgba(139,115,85,0.25);
    line-height: 1.3;
}}

.content h2 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 56px;
    font-weight: 800;
    color: #3d2b1f;
    margin: 40px 0 28px 0;
    padding-bottom: 16px;
    border-bottom: 2px solid rgba(139,115,85,0.25);
    line-height: 1.4;
}}

.content h2 .clause {{
    font-size: 40px;
    color: #8b7355;
    font-weight: 400;
    margin-right: 10px;
}}

.content h3 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 48px;
    font-weight: 700;
    color: #3d2b1f;
    margin: 36px 0 20px 0;
    line-height: 1.4;
}}

.content p {{ margin-bottom: 32px; }}

.content strong {{
    color: #b33a2b;
    font-weight: 700;
    border-bottom: 2px solid rgba(179,58,43,0.3);
}}

.content em {{
    font-style: italic;
    color: #8b7355;
}}

.content a {{
    color: #b33a2b;
    text-decoration: none;
    border-bottom: 2px solid rgba(179,58,43,0.3);
}}

.content ul, .content ol {{
    margin: 28px 0;
    padding-left: 48px;
}}

.content li {{
    margin-bottom: 16px;
    line-height: 1.8;
}}

.content li::marker {{
    color: #b33a2b;
    font-weight: 700;
}}

/* Blockquote — legal annotation style */
.content blockquote {{
    border-left: 5px solid #b33a2b;
    padding: 28px 32px;
    margin: 36px 0;
    background: rgba(179,58,43,0.04);
    color: #6b5a4a;
    position: relative;
    font-size: 40px;
}}

.content blockquote::before {{
    content: '按';
    position: absolute;
    top: -14px;
    left: 20px;
    font-size: 22px;
    color: #b33a2b;
    background: #f5f0e1;
    padding: 0 8px;
    font-weight: 700;
    letter-spacing: 2px;
}}

.content blockquote p {{ margin: 0; }}

/* Strikethrough + insertion */
.content del {{
    color: #a89880;
    text-decoration: line-through;
}}

.content ins {{
    color: #b33a2b;
    text-decoration: none;
    font-weight: 600;
}}

.content code {{
    background: rgba(139,115,85,0.1);
    padding: 4px 12px;
    border-radius: 4px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 36px;
    color: #6b5a4a;
}}

.content pre {{
    background: #2c2418;
    color: #e7e0d0;
    padding: 36px;
    margin: 32px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-all;
    font-size: 28px;
    line-height: 1.5;
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
    margin: 28px 0;
    font-size: 34px;
    line-height: 1.5;
    table-layout: fixed;
    word-break: break-word;
}}

.content thead th {{
    background: #3d2b1f;
    color: #f5f0e1;
    font-weight: 700;
    padding: 14px 14px;
    text-align: left;
    font-size: 30px;
}}

.content tbody td {{
    padding: 12px 14px;
    border-bottom: 1px solid rgba(139,115,85,0.25);
    vertical-align: top;
}}

.content tbody tr:nth-child(odd) td {{
    background: rgba(139,115,85,0.04);
}}

.content tbody tr:last-child td {{
    border-bottom: 3px solid #8b7355;
}}

.content td code, .content th code {{
    font-size: 26px;
    padding: 2px 6px;
    background: rgba(255,255,255,0.4);
    color: #6b5a4a;
}}

.content hr {{
    border: none;
    height: 0;
    border-bottom: 1px solid rgba(139,115,85,0.3);
    margin: 44px 0;
}}

.content img {{
    max-width: 100%;
    height: auto;
    margin: 32px auto;
    display: block;
}}

/* Tags */
.tags-container {{
    margin-top: 44px;
    padding-top: 28px;
    border-top: 1px solid rgba(139,115,85,0.3);
}}

.tag {{
    display: inline-block;
    background: rgba(179,58,43,0.08);
    color: #b33a2b;
    padding: 8px 20px;
    border-radius: 4px;
    font-size: 30px;
    margin: 6px 10px 6px 0;
    letter-spacing: 1px;
}}

/* Bane comment */
.bane-comment {{
    margin: 40px 0 0;
    text-align: right;
}}

.bane-comment img {{
    max-width: 55%;
    height: auto;
    border-radius: 8px;
    display: inline-block;
}}

.bane-comment .bane-caption {{
    font-size: 24px;
    color: #a89880;
    margin-top: 10px;
    line-height: 1.5;
    font-style: italic;
}}

/* Page number */
.page-number {{
    position: absolute;
    bottom: {int(height * 0.035)}px;
    right: {pad_x}px;
    font-size: 28px;
    color: #a89880;
}}
"""


def _cover_title_font_size(title: str, width: int) -> int:
    """Conservative title sizing to ensure single-line display on 9:16."""
    import re as _re
    clean = _re.sub(r'<[^>]+>', '', title)
    length = len(clean)
    if length <= 6:
        return int(width * 0.13)
    elif length <= 10:
        return int(width * 0.10)
    elif length <= 14:
        return int(width * 0.08)
    elif length <= 20:
        return int(width * 0.065)
    else:
        return int(width * 0.05)


def generate_cover(title, subtitle, first_section_html, width, height,
                   series_text="", stamp_text="待\u003cbr\u003e裁定"):
    t_size = _cover_title_font_size(title, width)
    css = _verdict_css(width, height)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>'

    series_html = ""
    if series_text:
        series_html = f'<div class="cover-series">{series_text}</div>'

    stamp_html = f'<div class="stamp">{stamp_text}</div>'

    body = f"""
    <div class="page cover-page">
        <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
        {subtitle_html}
        <div class="cover-body">{first_section_html}</div>
        {stamp_html}
        {series_html}
    </div>"""
    return html_document(body, css, width)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _verdict_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    content_html = _inject_clause_prefix(content_html)
    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
