"""Runtime Lab style: dark console layout for technical learning notes."""

import re

from styles.base import css_reset, font_imports, html_document, page_number_html

STYLE_NAME = "runtime-lab"
STYLE_DESCRIPTION = "Runtime Lab - dark console with cyan structure and amber emphasis"

BG = "#151820"
BG_DEEP = "#0c0f14"
PANEL = "#1b202a"
TEXT = "#e7e9ea"
MUTED = "#8f98a8"
CYAN = "#5eead4"
CYAN_DIM = "rgba(94,234,212,0.14)"
AMBER = "#fbbf24"
AMBER_DIM = "rgba(251,191,36,0.15)"
BORDER = "rgba(148,163,184,0.18)"


def _strip_leading_cover_heading(html_content: str, text: str) -> str:
    clean_text = re.sub(r"<[^>]+>", "", text).strip()
    if not clean_text:
        return html_content

    pattern = (
        r"^\s*<h[1-4][^>]*>\s*" + re.escape(clean_text) + r"\s*</h[1-4]>\s*"
    )
    return re.sub(pattern, "", html_content, count=1)


def _inject_step_marks(html_content: str) -> str:
    state = {"i": 0}

    def replace(match):
        state["i"] += 1
        attrs = match.group(1) or ""
        inner = match.group(2)
        return (
            f'<h2{attrs}>'
            f'<span class="step-mark">STEP {state["i"]:02d}</span>'
            f'<span class="step-title">{inner}</span>'
            "</h2>"
        )

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", replace, html_content)


def _is_reference_page(html_content: str) -> bool:
    reference_markers = (
        "引用章节：外部资料阅读顺序",
        "参考资料",
        "ZIO core reference",
        "Anthropic: Building effective agents",
        "PAgE 2026",
        "推荐阅读顺序",
    )
    return any(marker in html_content for marker in reference_markers)


def _title_em_width(title: str) -> float:
    text = re.sub(r"<br\s*/?>", "\n", title)
    lines = [re.sub(r"<[^>]+>", "", line).strip() for line in text.split("\n")]

    def line_width(line: str) -> float:
        width = 0.0
        for ch in line:
            if ch == " ":
                width += 0.28
            elif "\u4e00" <= ch <= "\u9fff" or ch in "，。、《》：；（）":
                width += 1.0
            else:
                width += 0.56
        return width

    return max((line_width(line) for line in lines if line), default=1.0)


def _cover_title_font_size(title: str, width: int) -> int:
    pad_x = int(width * 0.07)
    available = width - 2 * pad_x
    size = int(available * 0.94 / _title_em_width(title))
    return max(64, min(size, 128))


def _runtime_lab_css(width: int, height: int) -> str:
    pad_x = int(width * 0.072)
    pad_y = int(height * 0.04)
    return f"""
{css_reset()}
{font_imports(["Noto Sans SC", "Noto Serif SC", "JetBrains Mono"])}

body {{
    font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    width: {width}px;
    overflow: hidden;
    background: transparent;
}}

.page {{
    width: {width}px;
    min-height: {height}px;
    position: relative;
    overflow: hidden;
    padding: {pad_y}px {pad_x}px;
    background:
        radial-gradient(circle at 14% 10%, rgba(94,234,212,0.08), transparent 34%),
        radial-gradient(circle at 86% 92%, rgba(251,191,36,0.06), transparent 32%),
        repeating-linear-gradient(0deg, transparent 0, transparent 24px, rgba(255,255,255,0.025) 24px, rgba(255,255,255,0.025) 25px),
        {BG};
    color: {TEXT};
}}

.page::before {{
    content: '';
    position: absolute;
    left: {pad_x}px;
    right: {pad_x}px;
    top: {int(height * 0.027)}px;
    height: 3px;
    background: linear-gradient(90deg, {CYAN}, rgba(94,234,212,0.08));
}}

.page::after {{
    content: 'pl://learning-map';
    position: absolute;
    right: {pad_x}px;
    bottom: {int(height * 0.026)}px;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 18px;
    color: rgba(143,152,168,0.35);
    letter-spacing: 0.04em;
}}

.cover-page {{
    padding-top: {int(height * 0.065)}px;
}}

.cover-kicker {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 22px;
    color: {CYAN};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: 1px solid rgba(94,234,212,0.38);
    background: rgba(94,234,212,0.08);
    padding: 9px 16px;
    border-radius: 3px;
    margin-bottom: 42px;
}}

.cover-title {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-weight: 900;
    color: {TEXT};
    line-height: 1.18;
    margin-bottom: 20px;
    letter-spacing: 0;
}}

.cover-subtitle {{
    max-width: 880px;
    font-size: 35px;
    font-weight: 600;
    line-height: 1.48;
    color: {CYAN};
    margin-bottom: 42px;
}}

.cover-body {{
    color: {TEXT};
    font-size: 25px;
    line-height: 1.44;
    font-weight: 500;
}}

.cover-body h1:first-child {{
    display: none;
}}

.cover-body h4 {{
    font-size: 32px;
    line-height: 1.25;
    color: {AMBER};
    margin: 22px 0 10px;
}}

.cover-body p {{
    margin-bottom: 14px;
}}

.cover-rail {{
    position: absolute;
    left: {pad_x}px;
    right: {pad_x}px;
    bottom: {int(height * 0.067)}px;
    z-index: 2;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 16px;
    color: rgba(143,152,168,0.66);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background:
        linear-gradient(90deg, rgba(94,234,212,0.62), rgba(251,191,36,0.58))
        left 10px top 9px / 100% 1px no-repeat;
}}

.cover-rail-step {{
    position: relative;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.cover-rail-step::before {{
    content: '';
    width: 19px;
    height: 19px;
    border-radius: 50%;
    background: {BG};
    border: 2px solid {CYAN};
    box-shadow: 0 0 0 7px rgba(94,234,212,0.08);
}}

.cover-rail-step:last-child {{
    color: rgba(251,191,36,0.86);
}}

.cover-rail-step:last-child::before {{
    border-color: {AMBER};
    box-shadow: 0 0 0 7px rgba(251,191,36,0.10);
}}

.content {{
    position: relative;
    z-index: 1;
    color: {TEXT};
    font-size: 32px;
    line-height: 1.62;
    font-weight: 500;
}}

.content h1 {{
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-size: 60px;
    font-weight: 900;
    color: {TEXT};
    line-height: 1.22;
    margin-bottom: 34px;
}}

.content h2 {{
    display: grid;
    grid-template-columns: 150px 1fr;
    gap: 22px;
    align-items: start;
    margin: 46px 0 24px;
    padding: 20px 0 18px;
    border-top: 1px solid {BORDER};
    border-bottom: 1px solid {BORDER};
    line-height: 1.3;
}}

.content h2 .step-mark {{
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 20px;
    color: {AMBER};
    letter-spacing: 0.08em;
    padding-top: 8px;
}}

.content h2 .step-title {{
    font-size: 45px;
    font-weight: 800;
    color: {CYAN};
}}

.content h3 {{
    font-size: 38px;
    font-weight: 800;
    color: {AMBER};
    margin: 36px 0 16px;
    line-height: 1.35;
}}

.content p {{
    margin-bottom: 22px;
}}

.content strong {{
    color: {BG_DEEP};
    background: {AMBER};
    font-weight: 800;
    padding: 0 6px;
    border-radius: 2px;
}}

.content em {{
    color: {CYAN};
    font-style: normal;
}}

.content a {{
    color: {CYAN};
    text-decoration: none;
    border-bottom: 1px solid rgba(94,234,212,0.45);
}}

.content ul,
.content ol {{
    margin: 22px 0;
    padding-left: 46px;
}}

.content li {{
    margin-bottom: 12px;
    line-height: 1.56;
}}

.content li::marker {{
    color: {CYAN};
    font-weight: 800;
}}

.content code {{
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 27px;
    color: {CYAN};
    background: rgba(94,234,212,0.10);
    padding: 3px 9px;
    border-radius: 3px;
}}

.content pre {{
    position: relative;
    background: {BG_DEEP};
    border: 1px solid rgba(94,234,212,0.22);
    border-left: 5px solid {CYAN};
    padding: 34px 34px 30px;
    border-radius: 5px;
    margin: 30px 0;
    overflow-wrap: break-word;
    word-break: break-word;
    white-space: pre-wrap;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 25px;
    line-height: 1.48;
    color: {TEXT};
}}

.content pre::before {{
    content: '$ model';
    display: block;
    color: rgba(251,191,36,0.72);
    font-size: 18px;
    margin-bottom: 10px;
}}

.content pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    border-radius: 0;
    font-size: inherit;
}}

.content blockquote {{
    background: {PANEL};
    border-left: 5px solid {AMBER};
    padding: 28px 32px;
    margin: 32px 0;
    border-radius: 0 5px 5px 0;
    color: {AMBER};
}}

.content blockquote p {{
    margin: 0 0 14px;
    font-family: 'Noto Serif SC', 'Songti SC', serif;
    font-size: 34px;
    line-height: 1.5;
    font-weight: 700;
}}

.content blockquote p:last-child {{
    margin-bottom: 0;
}}

.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 28px 0;
    font-size: 24px;
    line-height: 1.42;
    background: rgba(12,15,20,0.62);
    border: 1px solid {BORDER};
}}

.content th {{
    color: {CYAN};
    background: rgba(94,234,212,0.09);
    font-weight: 800;
    text-align: left;
}}

.content th,
.content td {{
    border: 1px solid {BORDER};
    padding: 13px 14px;
    vertical-align: top;
}}

.content td:first-child {{
    color: {AMBER};
    font-weight: 700;
}}

.content hr {{
    border: none;
    height: 1px;
    background: {BORDER};
    margin: 44px 0;
}}

.tags-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 34px;
}}

.tag {{
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 22px;
    color: {CYAN};
    background: {CYAN_DIM};
    border: 1px solid rgba(94,234,212,0.26);
    padding: 5px 10px;
    border-radius: 3px;
}}

.page-number {{
    position: absolute;
    left: {pad_x}px;
    bottom: {int(height * 0.026)}px;
    z-index: 2;
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    font-size: 24px;
    color: {MUTED};
}}

.reference-page .content {{
    font-size: 24px;
    line-height: 1.28;
    font-weight: 500;
}}

.reference-page {{
    padding: 56px 62px;
}}

.reference-page .content h2 {{
    display: block;
    margin: 0 0 18px;
    padding: 0 0 14px;
    border-top: none;
    border-bottom: 1px solid {BORDER};
    font-size: 42px;
    line-height: 1.18;
    color: {CYAN};
}}

.reference-page .content h3 {{
    font-size: 29px;
    line-height: 1.22;
    margin: 18px 0 7px;
    color: {AMBER};
}}

.reference-page .content p {{
    margin-bottom: 10px;
}}

.reference-page .content ol,
.reference-page .content ul {{
    margin: 5px 0;
    padding-left: 28px;
}}

.reference-page .content li {{
    margin-bottom: 5px;
    line-height: 1.24;
}}

.reference-page .content table {{
    margin: 10px 0;
    font-size: 18px;
    line-height: 1.16;
}}

.reference-page .content th,
.reference-page .content td {{
    padding: 5px 7px;
}}

.reference-page .content code {{
    font-size: 20px;
    padding: 1px 4px;
}}
"""


def generate_cover(title, subtitle, first_section_html, width, height):
    css = _runtime_lab_css(width, height)
    cover_title = title or "Agent Runtime"
    t_size = _cover_title_font_size(cover_title, width)
    clean_body = _strip_leading_cover_heading(first_section_html, cover_title)
    clean_body = _strip_leading_cover_heading(clean_body, subtitle)
    subtitle_html = f'<div class="cover-subtitle">{subtitle}</div>' if subtitle else ""
    body = f"""
    <div class="page cover-page">
        <div class="cover-kicker">PL learning map</div>
        <div class="cover-title" style="font-size: {t_size}px;">{cover_title}</div>
        {subtitle_html}
        <div class="cover-body content">{clean_body}</div>
        <div class="cover-rail" aria-hidden="true">
            <div class="cover-rail-step">syntax</div>
            <div class="cover-rail-step">types</div>
            <div class="cover-rail-step">effects</div>
            <div class="cover-rail-step">runtime</div>
        </div>
    </div>"""
    return html_document(body, css, width)


def generate_card(content_html, page_number, total_pages, width, height):
    css = _runtime_lab_css(width, height)
    marked_html = _inject_step_marks(content_html)
    page_class = "page reference-page" if _is_reference_page(content_html) else "page"
    page_num = page_number_html(page_number, total_pages)
    body = f"""
    <div class="{page_class}">
        <div class="content">{marked_html}</div>
        {page_num}
    </div>"""
    return html_document(body, css, width)
