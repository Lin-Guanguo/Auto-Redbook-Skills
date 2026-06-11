"""Roadmap style — 路线图风格: light bg, three-color route system, station markers, dot grid."""

import re as _re

from styles.base import css_reset, font_imports, html_document, page_number_html

STYLE_NAME = "roadmap"
STYLE_DESCRIPTION = "路线图 — 亮色底 + 三色路线系统，工程架构路线图"
COVER_HEIGHT = 1920

# Text accent colors (darker shades for readability on light bg)
_AMBER = "#b45309"
_CYAN = "#0e7490"
_EMERALD = "#047857"

# Vibrant decorative colors (for dots, bars, station markers)
_VIB_A = "#f59e0b"
_VIB_B = "#06b6d4"
_VIB_C = "#10b981"


def _inject_station_markers(html_content: str) -> str:
    """Add colored station dot markers to h2 headings, cycling through route colors."""
    colors = [_VIB_A, _VIB_B, _VIB_C]
    state = {"i": 0}

    def _replace(m):
        color = colors[state["i"] % 3]
        state["i"] += 1
        attrs = m.group(1) or ""
        inner = m.group(2)
        return (
            f'<h2{attrs}>'
            f'<span class="station" style="background:{color};'
            f'box-shadow:0 0 10px {color}44;"></span>'
            f"{inner}</h2>"
        )

    return _re.sub(r"<h2([^>]*)>(.*?)</h2>", _replace, html_content)


def _cover_title_font_size(title: str, width: int, height: int) -> int:
    lines = _re.sub(r"<br\s*/?>", "\n", title).split("\n")

    def line_em_width(line: str) -> float:
        clean = _re.sub(r"<[^>]+>", "", line).strip()
        width = 0.0
        for ch in clean:
            if ch == " ":
                width += 0.28
            elif "\u4e00" <= ch <= "\u9fff" or ch in "，。、《》：；（）？":
                width += 1.0
            else:
                width += 0.56
        return width

    longest = max((line_em_width(line) for line in lines if line.strip()), default=1.0)
    available = width - int(width * 0.12) - 20
    size = int(available * 0.86 / longest)
    max_size = 76 if height <= 900 else 90
    min_size = 56 if height <= 900 else 64
    return max(min_size, min(size, max_size))


def _strip_cover_repeated_heading(html_content: str, title: str, subtitle: str) -> str:
    """Avoid rendering source title/subtitle twice on the cover."""
    if title:
        clean_title = _re.sub(r"<br\s*/?>", "", title)
        clean_title = _re.sub(r"<[^>]+>", "", clean_title)
        html_content = _re.sub(
            r"^\s*<h1[^>]*>\s*" + _re.escape(clean_title) + r"\s*</h1>\s*",
            "",
            html_content,
            count=1,
        )

    if subtitle:
        html_content = _re.sub(
            r"^\s*<p>\s*副标题：.*?</p>\s*",
            "",
            html_content,
            count=1,
        )

    return html_content


def _roadmap_css(width: int, height: int) -> str:
    pad_x = int(width * 0.06)
    pad_top = int(height * 0.04)
    compact_cover = height <= 900
    cover_title_margin = 14 if compact_cover else 22
    cover_subtitle_size = 39 if compact_cover else 46
    cover_subtitle_margin = 18 if compact_cover else 28
    cover_body_size = 27 if compact_cover else 36
    cover_body_line_height = 1.38 if compact_cover else 1.48
    route_line_height = 22 if compact_cover else 32
    route_line_margin = 7 if compact_cover else 12
    route_dot_size = 11 if compact_cover else 16
    route_label_size = 15 if compact_cover else 20
    route_label_display = "none" if compact_cover else "block"

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
    background: #f8fafc;
    position: relative;
    padding: {pad_top}px {pad_x}px;
    background-image:
        radial-gradient(circle, rgba(0,0,0,0.035) 1px, transparent 1px);
    background-size: 24px 24px;
}}

/* Tri-color gradient bar at top of content pages */
.page:not(.cover-page)::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {_VIB_A}, {_VIB_B}, {_VIB_C});
    opacity: 0.7;
}}

/* ---- Cover ---- */
.cover-page {{
    padding-top: {int(height * 0.05)}px;
}}

.route-lines {{
    position: absolute;
    bottom: {int(height * 0.05)}px;
    left: {pad_x}px;
    right: {pad_x}px;
}}

.route-line {{
    display: flex;
    align-items: center;
    margin-bottom: {route_line_margin}px;
    height: {route_line_height}px;
}}

.route-dot {{
    width: {route_dot_size}px;
    height: {route_dot_size}px;
    border-radius: 50%;
    flex-shrink: 0;
    margin-right: 14px;
}}

.route-bar {{
    flex: 1;
    height: 4px;
    border-radius: 2px;
    opacity: 0.6;
}}

.route-label {{
    display: {route_label_display};
    font-size: {route_label_size}px;
    color: rgba(0,0,0,0.3);
    margin-left: 14px;
    flex-shrink: 0;
    letter-spacing: 2px;
    min-width: 200px;
    text-align: right;
}}

.cover-title {{
    font-weight: 900;
    color: #0f172a;
    line-height: 1.14;
    margin-bottom: {cover_title_margin}px;
}}

.cover-subtitle {{
    display: block;
    font-size: {cover_subtitle_size}px;
    color: #1e293b;
    margin-bottom: {cover_subtitle_margin}px;
    line-height: 1.28;
    padding: 10px 0 22px;
    border-bottom: 1px solid rgba(0,0,0,0.08);
}}

.cover-subtitle .subtitle-text {{
    display: block;
    font-weight: 900;
}}

.cover-body {{
    color: #334155;
    font-size: {cover_body_size}px;
    line-height: {cover_body_line_height};
}}

.cover-body p {{ margin-bottom: 10px; }}

.cover-body strong {{
    color: {_AMBER};
    font-weight: 700;
    background: linear-gradient(to top, rgba(245,158,11,0.18) 40%, transparent 40%);
    padding: 0 2px;
}}

.cover-body em {{
    font-style: italic;
    color: {_CYAN};
}}

.cover-body h2 {{
    font-size: 38px;
    font-weight: 800;
    color: #0f172a;
    margin: 28px 0 16px 0;
    line-height: 1.3;
}}

.cover-body h3 {{
    font-size: 33px;
    font-weight: 700;
    color: #1e293b;
    margin: 20px 0 12px 0;
}}

.cover-body ul, .cover-body ol {{
    margin: 14px 0;
    padding-left: 40px;
}}

.cover-body li {{
    margin-bottom: 4px;
    line-height: 1.45;
}}

.cover-body li::marker {{
    color: {_EMERALD};
    font-weight: 700;
}}

.cover-body code {{
    background: rgba(14,116,144,0.08);
    padding: 2px 8px;
    border-radius: 3px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 28px;
    color: {_CYAN};
}}

.cover-body blockquote {{
    border: none;
    padding: 0;
    margin: 0;
    background: transparent;
    color: #334155;
    font-size: 36px;
}}
.cover-body blockquote p {{ margin: 0 0 18px 0; }}

.cover-badge {{
    position: absolute;
    bottom: {int(height * 0.04)}px;
    right: {pad_x}px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    color: #94a3b8;
    letter-spacing: 2px;
}}

.cover-badge .badge-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: {_VIB_B};
}}

/* ---- Content ---- */
.content {{
    color: #334155;
    font-size: 40px;
    line-height: 1.64;
}}

.content h1 {{
    font-size: 60px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 28px;
    line-height: 1.3;
}}

.content h2 {{
    font-size: 49px;
    font-weight: 800;
    color: #0f172a;
    margin: 32px -{pad_x}px 18px -{pad_x}px;
    padding: 16px {pad_x}px;
    line-height: 1.35;
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(0,0,0,0.025);
}}

.content h2 .station {{
    display: inline-block;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    flex-shrink: 0;
}}

.content h3 {{
    font-size: 42px;
    font-weight: 700;
    color: #1e293b;
    margin: 28px 0 14px 0;
    line-height: 1.35;
    padding-left: 16px;
    border-left: 4px solid {_VIB_B};
}}

.content p {{ margin-bottom: 22px; }}

.content strong {{
    color: {_AMBER};
    font-weight: 700;
    background: linear-gradient(to top, rgba(245,158,11,0.18) 40%, transparent 40%);
    padding: 0 2px;
}}

.content em {{
    font-style: italic;
    color: {_CYAN};
}}

.content a {{
    color: {_CYAN};
    text-decoration: none;
    border-bottom: 1px solid rgba(14,116,144,0.3);
}}

.content ul, .content ol {{
    margin: 18px 0;
    padding-left: 40px;
}}

.content li {{
    margin-bottom: 12px;
    line-height: 1.65;
}}

.content li::marker {{
    color: {_EMERALD};
    font-weight: 700;
}}

/* Blockquote */
.content blockquote {{
    border-left: 4px solid {_VIB_C};
    padding: 18px 28px;
    margin: 22px 0;
    background: rgba(16,185,129,0.04);
    color: #475569;
    font-size: 34px;
    border-radius: 0 6px 6px 0;
}}

.content blockquote p {{ margin: 0; }}

.content blockquote strong {{
    color: {_EMERALD};
    background: linear-gradient(to top, rgba(16,185,129,0.18) 40%, transparent 40%);
    padding: 0 2px;
}}

/* Code */
.content code {{
    background: rgba(14,116,144,0.08);
    padding: 2px 8px;
    border-radius: 3px;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 32px;
    color: {_CYAN};
}}

.content pre {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 32px;
    margin: 20px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-all;
    font-size: 26px;
    line-height: 1.45;
}}

.content pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: inherit;
}}

/* Tables — compact */
.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 28px;
    line-height: 1.4;
    table-layout: fixed;
    word-break: break-word;
}}

.content thead th {{
    background: rgba(6,182,212,0.08);
    color: #0f172a;
    font-weight: 700;
    padding: 8px 10px;
    text-align: left;
    font-size: 26px;
    border-bottom: 2px solid rgba(6,182,212,0.2);
}}

.content tbody td {{
    padding: 7px 10px;
    border-bottom: 1px solid rgba(0,0,0,0.06);
    vertical-align: top;
}}

.content tbody tr:nth-child(odd) td {{
    background: rgba(0,0,0,0.015);
}}

.content tbody tr:last-child td {{
    border-bottom: 2px solid rgba(0,0,0,0.1);
}}

.content td code, .content th code {{
    font-size: 24px;
    padding: 1px 4px;
    background: rgba(14,116,144,0.06);
    color: {_CYAN};
}}

.content hr {{
    border: none;
    height: 0;
    border-bottom: 1px solid rgba(0,0,0,0.08);
    margin: 30px 0;
}}

.content img {{
    max-width: 100%;
    height: auto;
    margin: 20px auto;
    display: block;
}}

/* Tags */
.tags-container {{
    margin-top: 28px;
    padding-top: 18px;
    border-top: 1px solid rgba(0,0,0,0.08);
}}

.tag {{
    display: inline-block;
    background: rgba(6,182,212,0.06);
    color: {_CYAN};
    padding: 5px 14px;
    border-radius: 3px;
    font-size: 24px;
    margin: 4px 8px 4px 0;
    letter-spacing: 1px;
}}

/* Route indicator (bottom-left of content pages) */
.route-indicator {{
    position: absolute;
    bottom: {int(height * 0.032)}px;
    left: {pad_x}px;
    display: flex;
    gap: 7px;
    align-items: center;
}}

.route-indicator span {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
}}

/* Page number */
.page-number {{
    position: absolute;
    bottom: {int(height * 0.03)}px;
    right: {pad_x}px;
    font-size: 24px;
    color: #94a3b8;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    t_size = _cover_title_font_size(title, width, height)
    css = _roadmap_css(width, height)
    cover_body = _strip_cover_repeated_heading(first_section_html, title, subtitle)

    route_lines_html = f"""
    <div class="route-lines">
        <div class="route-line">
            <div class="route-dot" style="background:{_VIB_A};box-shadow:0 0 6px {_VIB_A}55;"></div>
            <div class="route-bar" style="background:linear-gradient(90deg, {_VIB_A}, {_VIB_A}11);"></div>
            <span class="route-label">LOW-CODE</span>
        </div>
        <div class="route-line">
            <div class="route-dot" style="background:{_VIB_B};box-shadow:0 0 6px {_VIB_B}55;"></div>
            <div class="route-bar" style="background:linear-gradient(90deg, {_VIB_B}, {_VIB_B}11);"></div>
            <span class="route-label">SINGLE-AGENT</span>
        </div>
        <div class="route-line">
            <div class="route-dot" style="background:{_VIB_C};box-shadow:0 0 6px {_VIB_C}55;"></div>
            <div class="route-bar" style="background:linear-gradient(90deg, {_VIB_C}, {_VIB_C}11);"></div>
            <span class="route-label">MULTI-AGENT</span>
        </div>
    </div>"""

    subtitle_html = ""
    if subtitle:
        subtitle_html = (
            '<div class="cover-subtitle">'
            f'<span class="subtitle-text">{subtitle}</span>'
            '</div>'
        )

    badge_html = "" if height <= 900 else """
    <div class="cover-badge">
        <span class="badge-dot"></span>
        ROUTE MAP
    </div>"""

    body = f"""
    <div class="page cover-page">
        <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
        {subtitle_html}
        <div class="cover-body">{cover_body}</div>
        {route_lines_html}
        {badge_html}
    </div>"""
    return html_document(body, css, width)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _roadmap_css(width, height)
    page_num = page_number_html(page_number, total_pages)
    content_html = _inject_station_markers(content_html)

    route_indicator = f"""
    <div class="route-indicator">
        <span style="background:{_VIB_A}"></span>
        <span style="background:{_VIB_B}"></span>
        <span style="background:{_VIB_C}"></span>
    </div>"""

    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {route_indicator}
        {page_num}
    </div>"""
    return html_document(body, css, width)
