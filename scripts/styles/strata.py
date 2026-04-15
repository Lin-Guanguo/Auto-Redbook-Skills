"""Strata style — 技术地层: aged paper, era bands, year markers, archive catalog numbers."""

import re as _re

from styles.base import css_reset, font_imports, html_document

STYLE_NAME = "strata"
STYLE_DESCRIPTION = "技术地层 — 牛皮纸底 + 靛蓝墨 + 铜锈红 + 赭金徽标，史料册籍质感"
COVER_HEIGHT = 1920

# Palette
_INK = "#1e2a4a"        # deep indigo
_INK_DEEP = "#101a36"
_RUST = "#a13a1f"       # rust red
_OCHRE = "#c9a24a"      # ochre/gold
_PAPER = "#f5efde"      # aged cream
_PAPER_DEEP = "#ebe3cd"
_BODY = "#2b2a26"
_MUTED = "#8a7e64"
_SEPIA = "#5c4a2a"

# Roman numerals for era bands (supports 1..9)
_ROMAN = ["", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ"]


def _inject_era_marks(html_content: str) -> str:
    """Prefix h2 headings with a stratum marker § Ⅱ."""
    state = {"i": 0}

    def _replace(m):
        state["i"] += 1
        attrs = m.group(1) or ""
        inner = m.group(2)
        numeral = _ROMAN[state["i"]] if state["i"] < len(_ROMAN) else str(state["i"])
        return (
            f'<h2{attrs}>'
            f'<span class="stratum-mark">§ {numeral}</span>'
            f'<span class="stratum-title">{inner}</span>'
            f"</h2>"
        )

    return _re.sub(r"<h2([^>]*)>(.*?)</h2>", _replace, html_content)


def _cover_title_font_size(title: str, width: int, pad_x: int) -> int:
    # Compute font-size based on longest line's approximate em-width.
    lines = _re.split(r"<br\s*/?>", title)
    clean_lines = [_re.sub(r"<[^>]+>", "", l).strip() for l in lines if l.strip()]

    def line_em_width(s: str) -> float:
        em = 0.0
        for ch in s:
            if ch == " ":
                em += 0.28
            elif "\u4e00" <= ch <= "\u9fff" or ch in "——（）：；，。":
                em += 1.0
            else:
                em += 0.56
        return em

    max_em = max((line_em_width(l) for l in clean_lines), default=1.0)
    available = width - 2 * pad_x
    # 0.95 fills more aggressively since letter-spacing is -1px
    size = int(available * 0.95 / max(max_em, 1.0))
    return max(48, min(size, 150))


def _strata_css(width: int, height: int) -> str:
    pad_x = int(width * 0.06)
    pad_top = int(height * 0.05)

    return f"""
{css_reset()}
{font_imports(["Noto Serif SC", "Noto Sans SC", "JetBrains Mono"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
    width: {width}px;
    overflow: hidden;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: {_PAPER};
    position: relative;
    padding: {pad_top}px {pad_x}px;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent 0,
            transparent 94px,
            rgba(92,74,42,0.07) 94px,
            rgba(92,74,42,0.07) 95px
        ),
        radial-gradient(ellipse at 18% 12%, rgba(92,74,42,0.05), transparent 60%),
        radial-gradient(ellipse at 82% 88%, rgba(161,58,31,0.04), transparent 60%);
    color: {_BODY};
}}

/* Top era rule */
.page::before {{
    content: '';
    position: absolute;
    top: {int(height * 0.032)}px;
    left: {pad_x}px;
    right: {pad_x}px;
    height: 7px;
    border-top: 3px solid {_INK};
    border-bottom: 1px solid {_INK};
}}

/* Bottom rule */
.page::after {{
    content: '';
    position: absolute;
    bottom: {int(height * 0.032)}px;
    left: {pad_x}px;
    right: {pad_x}px;
    height: 0;
    border-bottom: 1px solid rgba(30,42,74,0.4);
}}

/* ---- Cover ---- */
.cover-page {{
    padding-top: {int(height * 0.05)}px;
}}

.cover-meta {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 19px;
    color: {_MUTED};
    letter-spacing: 3px;
    margin-bottom: 24px;
    text-transform: uppercase;
}}

.cover-meta .cat {{ color: {_RUST}; font-weight: 700; }}

.cover-title {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-weight: 900;
    color: {_INK_DEEP};
    line-height: 1.2;
    margin-bottom: 18px;
    letter-spacing: -1px;
}}

.cover-subtitle {{
    font-family: 'Noto Serif SC', serif;
    font-size: 38px;
    color: {_SEPIA};
    line-height: 1.5;
    margin-bottom: 32px;
    padding-bottom: 24px;
    padding-left: 20px;
    border-left: 5px solid {_OCHRE};
    font-style: italic;
}}

.cover-body {{
    color: {_BODY};
    font-size: 38px;
    line-height: 1.6;
}}

.cover-body p {{ margin-bottom: 22px; }}

.cover-body strong {{
    font-weight: 700;
    color: {_RUST};
    background: linear-gradient(to top, rgba(201,162,74,0.28) 35%, transparent 35%);
    padding: 0 3px;
}}

.cover-body em {{
    font-style: italic;
    color: {_INK};
}}

.cover-body blockquote {{
    border: none;
    padding: 12px 0 12px 26px;
    margin: 18px 0;
    background: transparent;
    color: {_INK_DEEP};
    font-size: 34px;
    line-height: 1.55;
    font-style: italic;
    border-left: 5px solid {_RUST};
    font-weight: 500;
}}
.cover-body blockquote p {{ margin: 0 0 12px 0; }}
.cover-body blockquote p:last-child {{ margin-bottom: 0; }}

.cover-body ul, .cover-body ol {{
    margin: 18px 0;
    padding-left: 40px;
}}
.cover-body li {{ margin-bottom: 10px; line-height: 1.6; }}
.cover-body li::marker {{ color: {_RUST}; font-weight: 700; }}

.cover-body hr {{
    border: none;
    height: 2px;
    background: {_INK};
    margin: 32px 0;
    opacity: 0.3;
}}

/* Year timeline at bottom of cover */
.timeline {{
    position: absolute;
    bottom: {int(height * 0.07)}px;
    left: {pad_x}px;
    right: {pad_x}px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding-bottom: 14px;
    border-bottom: 2px solid {_INK};
}}

.timeline-item {{
    font-family: 'JetBrains Mono', monospace;
    text-align: center;
    color: {_INK};
    position: relative;
}}

.timeline-year {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 1px;
}}

.timeline-label {{
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 15px;
    color: {_MUTED};
    letter-spacing: 2px;
    margin-top: 3px;
}}

.timeline-item::after {{
    content: '';
    position: absolute;
    bottom: -19px;
    left: 50%;
    transform: translateX(-50%);
    width: 9px;
    height: 9px;
    background: {_RUST};
    border-radius: 50%;
    border: 2px solid {_PAPER};
    box-shadow: 0 0 0 2px {_RUST};
}}

.cover-series {{
    position: absolute;
    bottom: {int(height * 0.022)}px;
    left: pad_x;
    width: 100%;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 19px;
    color: {_MUTED};
    letter-spacing: 4px;
}}

/* ---- Content ---- */
.content {{
    color: {_BODY};
    font-size: 29px;
    line-height: 1.56;
}}

.content h1 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 44px;
    font-weight: 900;
    color: {_INK_DEEP};
    margin: 4px 0 20px 0;
    padding-bottom: 14px;
    border-bottom: 3px double {_INK};
    line-height: 1.28;
}}

/* H2 = 章节带: generous top gap so mid-card chapter breaks breathe */
.content h2 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 33px;
    font-weight: 800;
    color: #ffffff;
    background: {_INK};
    margin: 36px -{pad_x}px 16px;
    padding: 12px {pad_x}px;
    line-height: 1.32;
    display: flex;
    align-items: baseline;
    gap: 14px;
    border-top: 3px solid {_OCHRE};
    border-bottom: 3px solid {_OCHRE};
}}

/* First h2 on a card needs less top margin */
.content > h2:first-child {{
    margin-top: 0;
}}

.content h2 .stratum-mark {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    color: {_OCHRE};
    letter-spacing: 2px;
    flex-shrink: 0;
    min-width: 68px;
}}

.content h2 .stratum-title {{
    flex: 1;
}}

.content h3 {{
    font-family: 'Noto Serif SC', serif;
    font-size: 31px;
    font-weight: 700;
    color: {_INK_DEEP};
    margin: 16px 0 10px 0;
    padding-left: 14px;
    border-left: 5px solid {_RUST};
    line-height: 1.3;
}}

.content p {{ margin-bottom: 10px; }}

.content strong {{
    font-weight: 700;
    color: {_RUST};
    background: linear-gradient(to top, rgba(201,162,74,0.28) 35%, transparent 35%);
    padding: 0 3px;
}}

.content em {{
    font-style: italic;
    color: {_INK};
}}

.content a {{
    color: {_RUST};
    text-decoration: none;
    border-bottom: 1px dashed {_RUST};
}}

.content ul, .content ol {{
    margin: 10px 0;
    padding-left: 38px;
}}

.content li {{
    margin-bottom: 5px;
    line-height: 1.5;
}}

.content li::marker {{
    color: {_RUST};
    font-weight: 700;
}}

/* Blockquote — "按" annotation */
.content blockquote {{
    border: none;
    border-left: 5px solid {_OCHRE};
    padding: 16px 24px 16px 28px;
    margin: 20px 0;
    background: rgba(201,162,74,0.08);
    color: {_SEPIA};
    font-size: 27px;
    line-height: 1.55;
    position: relative;
    font-style: italic;
}}

.content blockquote::before {{
    content: '笺';
    position: absolute;
    top: -11px;
    left: 12px;
    font-family: 'Noto Serif SC', serif;
    font-size: 18px;
    color: {_RUST};
    background: {_PAPER};
    padding: 0 8px;
    font-weight: 700;
    letter-spacing: 2px;
    font-style: normal;
}}

.content blockquote p {{ margin: 0 0 8px 0; }}
.content blockquote p:last-child {{ margin-bottom: 0; }}

.content blockquote strong {{
    color: {_INK_DEEP};
    background: linear-gradient(to top, rgba(201,162,74,0.4) 35%, transparent 35%);
}}

/* Inline code */
.content code {{
    background: {_PAPER_DEEP};
    padding: 2px 8px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 26px;
    color: {_INK};
    border: 1px solid rgba(30,42,74,0.15);
}}

/* Code blocks — archived-film feel */
.content pre {{
    background: {_INK_DEEP};
    color: #e8dfc5;
    padding: 20px;
    margin: 20px -{pad_x}px;
    padding-left: {pad_x}px;
    padding-right: {pad_x}px;
    white-space: pre;
    overflow: hidden;
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px;
    line-height: 1.45;
    border-left: 5px solid {_OCHRE};
    border-right: 5px solid {_OCHRE};
}}

.content pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: inherit;
    border: none;
}}

/* Tables — ledger/册籍 style */
.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0;
    font-size: 24px;
    line-height: 1.4;
    table-layout: fixed;
    word-break: break-word;
    border: 2px solid {_INK};
}}

.content thead th {{
    background: {_INK};
    color: {_OCHRE};
    font-family: 'Noto Serif SC', serif;
    font-weight: 700;
    padding: 9px 11px;
    text-align: left;
    font-size: 23px;
    letter-spacing: 1px;
    border-right: 1px solid rgba(201,162,74,0.3);
}}

.content thead th:last-child {{ border-right: none; }}

.content tbody td {{
    padding: 9px 11px;
    border-bottom: 1px solid rgba(30,42,74,0.15);
    border-right: 1px solid rgba(30,42,74,0.08);
    vertical-align: top;
}}

.content tbody td:last-child {{ border-right: none; }}

.content tbody tr:nth-child(odd) td {{
    background: rgba(235,227,205,0.45);
}}

.content tbody tr:last-child td {{
    border-bottom: 2px solid {_INK};
}}

/* Compact tables: 5+ cols */
.content table.compact {{ font-size: 21px; }}
.content table.compact thead th {{ font-size: 20px; padding: 8px 9px; }}
.content table.compact tbody td {{ padding: 8px 9px; }}

.content td code, .content th code {{
    font-size: 20px;
    padding: 1px 5px;
    background: rgba(255,255,255,0.5);
    color: {_INK};
    border: none;
}}

.content thead th code {{
    color: {_OCHRE};
    background: rgba(255,255,255,0.08);
}}

.content hr {{
    border: none;
    height: 0;
    border-bottom: 1px solid rgba(30,42,74,0.25);
    border-top: 1px solid rgba(30,42,74,0.25);
    padding-top: 3px;
    margin: 14px 0;
}}

.content img {{
    max-width: 100%;
    height: auto;
    margin: 24px auto;
    display: block;
    border: 2px solid {_INK};
}}

/* Page marker — archive catalog */
.catalog {{
    position: absolute;
    bottom: {int(height * 0.052)}px;
    right: {pad_x}px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px;
    color: {_MUTED};
    letter-spacing: 3px;
}}

.catalog .num {{ color: {_RUST}; font-weight: 700; }}

.stratum-depth {{
    position: absolute;
    bottom: {int(height * 0.052)}px;
    left: {pad_x}px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    color: {_MUTED};
    letter-spacing: 3px;
    text-transform: uppercase;
}}
"""


TABLE_COMPACT_JS = """
document.querySelectorAll('.content table').forEach(t => {
    const cols = t.querySelector('tr') ? t.querySelector('tr').children.length : 0;
    if (cols >= 5) t.classList.add('compact');
});
"""


def generate_cover(title, subtitle, first_section_html, width, height, series_text=""):
    pad_x = int(width * 0.06)
    t_size = _cover_title_font_size(title, width, pad_x)
    css = _strata_css(width, height)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>'

    timeline_html = f"""
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-year">1974</div>
            <div class="timeline-label">KPN</div>
        </div>
        <div class="timeline-item">
            <div class="timeline-year">1985</div>
            <div class="timeline-label">SNAPSHOT</div>
        </div>
        <div class="timeline-item">
            <div class="timeline-year">2014</div>
            <div class="timeline-label">FLINK</div>
        </div>
        <div class="timeline-item">
            <div class="timeline-year">2024</div>
            <div class="timeline-label">AGENT</div>
        </div>
    </div>
    """

    series_html = f'<div class="cover-series">{series_text}</div>' if series_text else ""

    meta_html = f"""
    <div class="cover-meta">
        <span class="cat">STRATA · № 10</span>
        <span>TECH · LINEAGE · OBSERVATION</span>
    </div>
    """

    body = f"""
    <div class="page cover-page">
        {meta_html}
        <div class="cover-title" style="font-size: {t_size}px;">{title}</div>
        {subtitle_html}
        <div class="cover-body">{first_section_html}</div>
        {timeline_html}
        {series_html}
    </div>"""
    return html_document(body, css, width, scripts=TABLE_COMPACT_JS)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _strata_css(width, height)
    content_html = _inject_era_marks(content_html)

    catalog_html = f'<div class="catalog">№ <span class="num">{page_number:02d}</span> / {total_pages:02d}</div>'
    depth_html = f'<div class="stratum-depth">STRATA · LAYER {page_number:02d}</div>'

    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {depth_html}
        {catalog_html}
    </div>"""
    return html_document(body, css, width, scripts=TABLE_COMPACT_JS)
