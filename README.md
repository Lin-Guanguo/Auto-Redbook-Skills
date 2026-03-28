# Auto-Redbook-Skills

Markdown to image rendering tool for social media (Xiaohongshu, etc). Uses headless Chrome (Playwright) to render styled HTML into 9:16 vertical images.

## New Style System (`render.py`)

Each style is a self-contained Python module — fully controls layout, colors, fonts, and decorations. No shared HTML skeleton, no template limitations.

### Usage

```bash
python scripts/render.py input.md --style paper -o ./output
```

### Input Format

Markdown with YAML frontmatter. Use `---` to separate pages.

```markdown
---
title: "Article Title"
subtitle: "Optional subtitle"
---

First section (becomes cover page with large title).

---

Second section (page 2).

---

More sections...
```

- Page 1 (cover): title + subtitle + first section content
- Page 2+: one section per page
- Content height is dynamic — pages grow to fit, capped at `--max-height`

### Available Styles

| Style | Description |
|-------|-------------|
| `paper` | 笔记纸 — ruled lines + red margin line, warm paper background |

### Parameters

| Param | Short | Default | Description |
|-------|-------|---------|-------------|
| `--style` | `-s` | required | Style name |
| `--output-dir` | `-o` | cwd | Output directory |
| `--width` | `-w` | 1080 | Image width (px) |
| `--height` | | 1440 | Min image height (px) |
| `--max-height` | | 4320 | Max image height (px) |
| `--dpr` | | 2 | Device pixel ratio |

### Preview Styles

Generate an HTML page to visually compare all available styles:

```bash
python scripts/preview_styles.py          # opens in browser
python scripts/preview_styles.py -o preview.html  # save to file
```

### Adding a New Style

Create `scripts/styles/mystyle.py`:

```python
STYLE_NAME = "mystyle"
STYLE_DESCRIPTION = "My custom style"

def generate_cover(title, subtitle, first_section_html, width, height) -> str:
    """Return complete HTML for the cover page."""

def generate_card(content_html, page_number, total_pages, width, height) -> str:
    """Return complete HTML for content pages."""
```

Register in `scripts/styles/__init__.py`.

### Dependencies

```bash
pip install markdown pyyaml playwright
playwright install chromium
```

## Legacy Theme System (`render_xhs.py`)

The old rendering system with 11 CSS themes sharing a fixed HTML layout. Still works, documented in `README.old.md`.
