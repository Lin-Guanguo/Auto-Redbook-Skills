"""Essay style — 二次阅读的书本: cream bg, serif body, yellow highlighter bold, navy pullquotes."""

from styles.base import (
    css_reset,
    font_imports,
    html_document,
    page_number_html,
    title_font_size,
)

STYLE_NAME = "essay"
STYLE_DESCRIPTION = "随笔书卷 — 米黄纸底 + 藏蓝金句 + 荧光笔加粗"

BG = "#f5efe4"
TEXT = "#1a1a1a"
MUTED = "#5a5a5a"
HIGHLIGHT = "#ffe066"
ACCENT = "#2b3a5c"


def _essay_css(width: int, height: int) -> str:
    pad_x = int(width * 0.07)
    pad_y = int(height * 0.05)

    return f"""
{css_reset()}
{font_imports(["Noto Serif SC", "Noto Sans SC", "EB Garamond"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    width: {width}px;
    overflow: hidden;
    background: transparent;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    background: {BG};
    position: relative;
    padding: {pad_y}px {pad_x}px {pad_y}px {pad_x}px;
}}

/* ===== Cover ===== */
.cover-title-wrap {{
    line-height: 1.45;
    margin-bottom: 32px;
}}

.cover-title {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-weight: 900;
    color: {BG};
    background: {ACCENT};
    padding: 10px 22px;
    letter-spacing: 0.02em;
    box-decoration-break: clone;
    -webkit-box-decoration-break: clone;
}}

.cover-subtitle {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-weight: 700;
    font-size: 44px;
    color: {TEXT};
    line-height: 1.5;
    margin-bottom: 40px;
}}

.cover-divider {{
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 44px;
}}

.cover-divider .rule {{
    flex: 0 0 80px;
    height: 2px;
    background: {ACCENT};
}}

.cover-divider .fleuron {{
    color: {ACCENT};
    font-size: 40px;
    line-height: 1;
}}

/* ===== Content typography ===== */
.content {{
    color: {TEXT};
    font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    font-size: 36px;
    line-height: 1.6;
    font-weight: 500;
}}

.content h1 {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-size: 64px;
    font-weight: 900;
    color: {TEXT};
    margin-bottom: 32px;
    line-height: 1.3;
}}

.content h2 {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-size: 56px;
    font-weight: 700;
    color: {TEXT};
    margin: 50px 0 24px 0;
    line-height: 1.35;
    position: relative;
    text-align: center;
}}

.content h2::before {{
    content: '❧';
    display: block;
    color: {ACCENT};
    font-size: 34px;
    line-height: 1;
    margin-bottom: 12px;
    font-weight: 400;
}}

.content h3 {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-size: 44px;
    font-weight: 700;
    color: {TEXT};
    margin: 36px 0 18px 0;
    line-height: 1.4;
}}

.content p {{
    margin-bottom: 28px;
}}

.content strong {{
    font-weight: 700;
    color: {TEXT};
    background: linear-gradient(
        transparent 55%,
        {HIGHLIGHT} 55%,
        {HIGHLIGHT} 92%,
        transparent 92%
    );
    padding: 0 2px;
}}

.content em {{
    font-style: italic;
    color: {ACCENT};
}}

.content a {{
    color: {ACCENT};
    text-decoration: none;
    border-bottom: 2px solid {ACCENT};
}}

.content ul, .content ol {{
    margin: 24px 0;
    padding-left: 50px;
}}

.content li {{
    margin-bottom: 14px;
    line-height: 1.55;
}}

.content li::marker {{
    color: {ACCENT};
}}

/* ===== Pullquote (Q2) ===== */
.content blockquote {{
    border-top: 2px solid {ACCENT};
    border-bottom: 2px solid {ACCENT};
    padding: 50px 36px;
    margin: 50px 0;
    position: relative;
    text-align: center;
}}

.content blockquote::before {{
    content: '◆';
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    background: {BG};
    color: {ACCENT};
    font-size: 36px;
    line-height: 1;
    padding: 0 14px;
}}

.content blockquote p,
.content blockquote h1,
.content blockquote h2,
.content blockquote h3 {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-style: italic;
    font-size: 54px;
    line-height: 1.45;
    color: {ACCENT};
    margin: 0;
    text-align: center;
    font-weight: 400;
}}

.content blockquote strong {{
    /* Disable highlighter inside pullquote */
    background: none;
    color: {ACCENT};
    font-weight: 700;
    padding: 0;
}}

/* ===== Code ===== */
.content code {{
    background: rgba(0, 0, 0, 0.06);
    padding: 4px 12px;
    border-radius: 4px;
    font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    font-size: 36px;
    color: {TEXT};
}}

.content pre {{
    background: #2c2c2c;
    color: #e0e0e0;
    padding: 40px;
    border-radius: 8px;
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

.content hr {{
    border: none;
    height: 1px;
    background: rgba(0, 0, 0, 0.08);
    margin: 50px 0;
}}

.content img {{
    max-width: 100%;
    height: auto;
    margin: 35px auto;
    display: block;
}}

/* ===== Tables ===== */
.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 35px 0;
    font-size: 36px;
}}

.content th, .content td {{
    border-bottom: 1px solid rgba(0, 0, 0, 0.12);
    padding: 16px 12px;
    text-align: left;
    line-height: 1.5;
}}

.content th {{
    color: {ACCENT};
    font-weight: 700;
    border-bottom: 2px solid {ACCENT};
}}

/* ===== Chrome ===== */
.page-number {{
    position: absolute;
    bottom: {int(height * 0.035)}px;
    right: {pad_x}px;
    font-size: 32px;
    color: {ACCENT};
    font-family: 'EB Garamond', 'Noto Serif SC', serif;
    letter-spacing: 0.08em;
}}

.tags-container {{
    margin-top: 50px;
    padding-top: 30px;
    border-top: 1px solid rgba(0, 0, 0, 0.12);
}}

.tag {{
    display: inline-block;
    color: {ACCENT};
    border: 1px solid {ACCENT};
    padding: 8px 20px;
    border-radius: 4px;
    font-size: 30px;
    margin: 8px 12px 8px 0;
    font-family: 'EB Garamond', 'Noto Serif SC', serif;
}}
"""


def generate_cover(
    title: str,
    subtitle: str,
    first_section_html: str,
    width: int,
    height: int,
) -> str:
    t_size = title_font_size(title, width)
    css = _essay_css(width, height)

    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>'

    body = f"""
    <div class="page">
        <div class="cover-title-wrap">
            <span class="cover-title" style="font-size: {t_size}px;">{title}</span>
        </div>
        {subtitle_html}
        <div class="cover-divider">
            <div class="rule"></div>
            <div class="fleuron">❧</div>
            <div class="rule"></div>
        </div>
        <div class="content">{first_section_html}</div>
    </div>
    """
    return html_document(body, css, width)


def generate_card(
    content_html: str,
    page_number: int,
    total_pages: int,
    width: int,
    height: int,
) -> str:
    css = _essay_css(width, height)
    page_num = page_number_html(page_number, total_pages)

    body = f"""
    <div class="page">
        <div class="content">{content_html}</div>
        {page_num}
    </div>
    """
    return html_document(body, css, width)
