Last Updated: 2026-03-27

# Style System Design

## Background

The current project renders markdown to Xiaohongshu (小红书) 9:16 vertical images using Playwright. All 11 themes share the same HTML structure: gradient background → rounded rectangle card → content. This makes every output look visually identical regardless of theme.

This design introduces a new **style system** that gives each style full control over its visual output — layout, colors, fonts, decorations, cover design — as a self-contained Python module.

## Design Decisions

1. **Bundled/self-contained styles** — each style is a complete package (layout + colors + fonts + decorations). No orthogonal layout × theme composition. Simpler, and avoids bad combinations.

2. **Python function per style** — each style is a Python module exporting functions that return complete HTML strings. No template files. Full flexibility, no ceiling.

3. **New code, separate from old** — new entry point `render.py`, new `styles/` package. Old `render_xhs.py` and `assets/themes/` untouched.

4. **No empty cover page** — the cover is the first page with a prominent title + first section of content. Not a decorative splash page.

## Architecture

```
scripts/
├── render_xhs.py           # Old entry point. Untouched.
├── render.py                # New entry point.
├── styles/
│   ├── __init__.py          # Style registry
│   ├── base.py              # Shared utilities
│   ├── paper.py             # First style: 笔记纸
│   └── ...                  # Future styles
assets/
├── themes/                  # Old themes. Untouched.
```

### `render.py` — New Entry Point

Responsibilities:
- CLI parsing: `--style` (required), `-o`, `--width`, `--height`, `--dpr`
- Read and parse markdown (YAML frontmatter + body)
- Split body by `---` separators (first section → cover, rest → cards)
- Look up style module from registry, call its functions to get HTML
- Playwright rendering: HTML → headless Chrome → PNG screenshot

Reuses the same Playwright rendering approach as `render_xhs.py` (browser reuse, font caching, dynamic height calculation). Code is copied and adapted, not shared via imports.

```bash
python scripts/render.py input.md --style paper -o ./output
```

### `styles/` — Style Package

#### `__init__.py` — Registry

```python
from styles import paper

STYLES = {
    "paper": paper,
}

def get_style(name: str):
    """Returns the style module or raises ValueError."""
```

#### `base.py` — Shared Utilities

Common functions any style can use:

- `css_reset()` → CSS reset string
- `font_imports(fonts: list[str])` → Google Fonts `@import` statements
- `html_document(body: str, styles: str, width: int, scripts: str = "")` → wraps content in a complete `<!DOCTYPE html>` document
- `convert_markdown_to_html(md_text: str)` → markdown to HTML using `markdown` library with extensions (extra, codehilite, tables, nl2br)
- `title_font_size(title: str, width: int)` → dynamic font size based on title length
- `page_number_html(current: int, total: int)` → page number snippet

#### Style Module Interface

Each style module exports:

```python
STYLE_NAME: str          # e.g. "paper"
STYLE_DESCRIPTION: str   # e.g. "笔记纸风格 — 横线纸 + 左侧红线"

def generate_cover(title: str, subtitle: str, first_section_html: str,
                   width: int, height: int) -> str:
    """First page: prominent title + first section of content.
    Returns a complete HTML document string."""

def generate_card(content_html: str, page_number: int,
                  total_pages: int, width: int, height: int) -> str:
    """Subsequent pages: body content.
    content_html is already converted from markdown.
    Returns a complete HTML document string."""
```

### Content Flow

The rendering input is NOT the user's original markdown. There is a preparation step:

```
Original markdown (user's article, kept untouched)
    ↓
Preparation (AI-assisted, before render.py is called):
  - Add --- separators at logical page break points
  - Adjust formatting for image-based reading (e.g. heading levels)
  - NO content changes: every word of the original is preserved
    ↓
Rendering-ready markdown (with page breaks)
    ↓
render.py reads it:
  - Parse YAML frontmatter (title, subtitle) + body
  - Split body by --- separators (first section → cover, rest → cards)
  - Convert each section: markdown → HTML
    ↓
Page 1: style.generate_cover(title, subtitle, first_section_html, ...)
Page 2+: style.generate_card(section_html, page_num, total, ...)
    ↓
Playwright renders each HTML → PNG
    ↓
Output: page_1.png, page_2.png, ...
```

The preparation step is done by the user (with AI assistance) outside of `render.py`. The script itself only handles rendering — it expects a markdown file that already has `---` page separators in place.

## First Style: Paper (笔记纸)

Visual design:
- **Background**: warm paper color `#f4f0e8`, no gradient
- **Decorations**: horizontal ruled lines + left red margin line
- **No outer frame**: no rounded rectangle, no shadow, no gradient background
- **Font size**: optimized for phone reading — body ~42px, headings ~56-72px on 1080px canvas (same proportion as old project)
- **Cover (page 1)**: same paper background, title in large font, first section content below
- **Cards (page 2+)**: same paper background, section heading + body text
- **Page numbers**: bottom right, subtle color

## README Update

Add a new section describing the new style system separately from the old theme system. Include usage examples for `render.py`.
